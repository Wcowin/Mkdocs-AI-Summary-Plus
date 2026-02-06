"""Setup script for MkDocs AI Summary Plugin"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else ""

setup(
    name='mkdocs_ai_summary_wcowin',
    version='1.3.0',
    description='AI-powered summary generation plugin for MkDocs Material',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MkDocs AI Summary Team',
    author_email='support@mkdocs-ai-summary.com',
    url='https://github.com/Wcowin/Mkdocs-AI-Summary-Plus',
    license='MIT',
    
    packages=find_packages(),
    include_package_data=True,
    
    python_requires='>=3.8',
    install_requires=[
        'mkdocs>=1.4.0',
        'requests>=2.25.0',
        'python-dotenv>=0.19.0',
    ],
    
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'responses>=0.18.0',
        ],
    },
    
    entry_points={
        'mkdocs.plugins': [
            'ai-summary = mkdocs_ai_summary.plugin:AISummaryPlugin',
        ]
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Markup :: Markdown',
    ],
    
    keywords=[
        'mkdocs',
        'plugin',
        'ai',
        'summary',
        'documentation',
        'markdown',
        'material',
        'openai',
        'gemini',
        'deepseek',
        'glm',
    ],
    
    project_urls={
        'Documentation': 'https://github.com/Wcowin/Mkdocs-AI-Summary-Plus',
        'Source': 'https://github.com/Wcowin/Mkdocs-AI-Summary-Plus',
        'Tracker': 'https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/issues',
    },
)