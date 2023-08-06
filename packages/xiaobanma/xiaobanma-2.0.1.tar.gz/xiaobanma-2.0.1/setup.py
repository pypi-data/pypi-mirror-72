import setuptools

with open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(name='xiaobanma',
                 version='2.0.1',
                 description='markdown editor',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='Shiweihao',
                 author_email='shi-weihao@qq.com',
                 url='https://markdown.felinae.net',
                 keywords='django markdown editor editormd',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 include_package_data=True,
                 classifiers=(
                     "Programming Language :: Python",
                     "Development Status :: 4 - Beta",
                     "Operating System :: OS Independent",
                     "License :: OSI Approved :: Apache Software License",
                     "Framework :: Django"
                 ))
