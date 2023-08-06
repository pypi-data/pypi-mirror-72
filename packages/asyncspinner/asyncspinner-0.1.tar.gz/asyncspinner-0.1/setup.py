'''Installation script run by pip'''
from setuptools import setup, find_packages

def main():
    '''Begin setup'''
    setup(
        name='asyncspinner',
        version='0.1',
        packages=find_packages(),
        install_requires=[
            'colorama',
            'cursor',
        ],
        description='Little graphic to show user that something is waited for when '
                    'a progress bar is overkill, or the progress is unknown.',
        project_urls={
            'Source Code': 'https://github.com/Hegdahl/asyncspinner',
        },
        classifiers=[
            'License :: OSI Approved :: MIT License'
        ],
    )

if __name__ == "__main__":
    main()
