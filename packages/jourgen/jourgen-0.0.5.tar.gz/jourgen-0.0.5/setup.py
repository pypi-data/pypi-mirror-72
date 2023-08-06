from distutils.core import setup
setup(
    name='jourgen',
    packages=['jourgen'],
    entry_points={
        "console_scripts": ['jourgen = jourgen.jourgen:cli']
    },
    version='0.0.5',
    license='MIT',
    description='Tiny but functional blog engine',
    author='Pablo Toledo Margalef',
    author_email='pabloatm980@gmail.com',
    url='https://gitlab.com/papablo/journal-generator',
    download_url='https://gitlab.com/papablo/journal-generator/-/archive/0.0.5/journal-generator-0.0.5.tar.gz',
    keywords=['blogging', 'blog', 'writing'],
    install_requires=[
        'click',
        'Jinja2',
        'livereload',
        'Markdown',
        'Pygments',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Office/Business :: News/Diary',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
