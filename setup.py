from setuptools import setup, find_packages

setup(name='Assistant9',
    version='0.0.1',
    description= 'Addressbook, Notebook, Folder Sorter',
    url='https://github.com/Yurii-Potapchuk/Team_9',
    author='pass',
    author_email='pass',
    license='MIT',
    packages=find_packages(),
    entry_points= {'console_scripts': ['assistant = assistant.main_menu:menu']}
          )
