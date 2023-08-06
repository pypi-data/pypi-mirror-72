from setuptools import setup
from setuptools.extension import Extension

setup(name='custom_wordcloud_generator',
      version='0.1',
      description='Slightly modified Muellers Wordcloud generator',
      packages=['custom_wordcloud_generator'],
      author_email='ekertdenis@gmail.com',
      install_requires=['numpy>=1.6.1', 'pillow', 'matplotlib'],
      ext_modules=[Extension("wordcloud.query_integral_image",
                           ["wordcloud/query_integral_image.c"])],
      zip_safe=False)
