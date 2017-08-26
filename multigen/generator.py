"""Small framework for multifile generation on top of another template code generator."""
import logging
import os

from .formatter import format_raw

_logger = logging.getLogger(__name__)


class Generator:
    """
    Code generator from PyEcore models.
    
    Attributes:
        tasks:
            List of generator tasks to be processed as part of this generator.
    """

    tasks = []

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('Unexpected arguments: {!r}'.format(kwargs))

    def generate(self, model, outfolder):
        """
        Generate artifacts for given model.
        
        Attributes:
            model:
                Model for which to generate code.
            outfolder: 
                Folder where code files are created.
        """
        _logger.info('Generating code to {!r}.'.format(outfolder))

        for task in self.tasks:
            for element in task.filtered_elements(model):
                task.run(element, outfolder)


class Task:
    """
    File generation task applied to a set of model elements.
    
    Attributes:
        formatter: Callable converting this generator tasks raw output into a nicely formatted
                   string.
    """

    def __init__(self, formatter=None, **kwargs):
        if kwargs:
            raise AttributeError('Unexpected arguments: {!r}'.format(kwargs))
        self.formatter = formatter or format_raw

    def run(self, element, outfolder):
        """Apply this task to model element."""
        filepath = self.relative_path_for_element(element)
        if outfolder and not os.path.isabs(filepath):
            filepath = os.path.join(outfolder, filepath)

        _logger.debug('{!r} --> {!r}'.format(element, filepath))

        self.ensure_folder(filepath)
        self.generate_file(element, filepath)

    @staticmethod
    def ensure_folder(filepath):
        dirname = os.path.dirname(filepath)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def filtered_elements(self, model):
        """Iterator over model elements to execute this task for."""
        raise NotImplementedError()

    def relative_path_for_element(self, element):
        """Returns relative file path receiving the generator output for given element."""
        raise NotImplementedError()

    def generate_file(self, element, filepath):
        """Actual file generation from model element."""
        raise NotImplementedError()


class TemplateGenerator(Generator):
    templates_path = 'templates'

    def __init__(self, global_context=None, **kwargs):
        super().__init__(**kwargs)
        global_context = global_context or self.create_global_context()

        # pass optional global context to tasks:
        for task in self.tasks:
            task.global_context = global_context

    def create_global_context(self, **kwargs):
        """Model-wide code generation context, passed to all templates."""
        context = dict(**kwargs)
        return context


class TemplateFileTask(Task):
    """Task to generate code via a code-generator template.

    Attributes:
        template_name: Name of the template to use for this task.
        global_context: Template-independent context data, propagated by generator class.
    """
    template_name = None
    global_context = None

    def create_template_context(self, element, **kwargs):
        """Code generation context, specific to template and current element."""
        context = dict(element=element, **kwargs)
        if self.global_context:
            context.update(**self.global_context)
        return context
