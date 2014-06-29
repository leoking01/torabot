import jsonpickle
from jinja2 import Environment, PackageLoader
from ..base import Base


class Target(Base):

    def __init__(self, *args, **kargs):
        super(Target, self).__init__(*args, **kargs)
        self.jinja2_env = Environment(loader=PackageLoader(
            'torabot.core.make.targets.jinja2',
            'templates'
        ))
        self.jinja2_env.filters['tojson'] = jsonpickle.encode
        self.jinja2_env.globals['read_json'] = self.read_json

    @Base.preprocessed
    def __call__(self, template, kargs):
        return self.get_template_content(template).render(**kargs)

    def get_template_content(self, name_or_content):
        if isinstance(name_or_content, str):
            return self.jinja2_env.from_string(name_or_content)
        assert isinstance(name_or_content, dict), 'unknown type: {}'.format(type(name_or_content))
        name = name_or_content['name']
        try:
            return self.jinja2_env.get_template(name)
        except:
            return self.jinja2_env.from_string(self.read_text(name))