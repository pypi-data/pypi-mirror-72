from pathlib import Path, PurePath
from tempfile import TemporaryDirectory
import base64
import io
import re
import urllib.parse

import requests
from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
from traitlets import Instance, Unicode

from ._screenshot import make_repr_png

def get_image_files(md_source):
    '''
    Return all image files from a markdown cell

    Parameters
    ----------
    md_source : str
        Markdown text from cell['source']
    '''
    pat_inline = r'\!\[.*?\]\((.*?\.(?:gif|png|jpg|jpeg|tiff))'
    pat_ref = r'\[.*?\]:\s*(.*?\.(?:gif|png|jpg|jpeg|tiff))'
    inline_files = re.findall(pat_inline, md_source)
    ref_files = re.findall(pat_ref, md_source)
    possible_image_files = inline_files + ref_files
    image_files = []
    for file in possible_image_files:
        p = file.strip()
        if p not in image_files and not p.startswith('attachment') and not p.startswith('http'):
            image_files.append(p)
    return image_files

def get_image_tags(md_source):
    pat_img_tag = r'''(<img.*?[sS][rR][Cc]\s*=\s*['"](.*?)['"].*?/>)'''
    img_tag_files = re.findall(pat_img_tag, md_source)
    return img_tag_files

class MarkdownPreprocessor(Preprocessor):

    output_dir = Instance(klass=PurePath)
    image_dir_name = Instance(klass=PurePath)

    def preprocess_cell(self, cell, resources, cell_index):
        nb_home = Path(resources['metadata']['path'])
        if cell['cell_type'] == 'markdown':

            # find normal markdown images 
            all_image_files = get_image_files(cell['source'])
            for i, image_file in enumerate(all_image_files):
                image_data = open(nb_home / image_file, 'rb').read()
                ext = Path(image_file).suffix
                    
                new_image_name = f'markdown_{cell_index}_normal_image_{i}{ext}'
                final_image_fn = self.output_dir / new_image_name
                with open(final_image_fn, 'wb') as f:
                    f.write(image_data)
                image_dir = self.image_dir_name / new_image_name
                replace_str = urllib.parse.quote(str(image_dir))
                cell['source'] = cell['source'].replace(image_file, replace_str)

            # find HTML <img> tags
            all_image_tag_files = get_image_tags(cell['source'])
            for i, (entire_tag, src) in enumerate(all_image_tag_files):
                if src.startswith('http'):
                    replace_str = f'![]({src})'
                else:
                    image_data = open(nb_home / src, 'rb').read()
                    ext = Path(src).suffix
                    new_image_name = f'markdown_{cell_index}_html_image_tag_{i}{ext}'
                    final_image_fn = self.output_dir / new_image_name
                    with open(final_image_fn, 'wb') as f:
                        f.write(image_data)
                
                    image_dir = self.image_dir_name / new_image_name
                    image_dir = urllib.parse.quote(str(image_dir))
                    replace_str = f'![]({image_dir})'
                    
                cell['source'] = cell['source'].replace(entire_tag, replace_str)

            # find images attached to markdown through dragging and dropping
            attachments = cell.get('attachments', {})
            for i, (image_name, data) in enumerate(attachments.items()):
                # I think there is only one image per attachment
                # Though there can be multiple attachments per cell
                # So, this should only loop once
                for j, (mime_type, base64_data) in enumerate(data.items()):
                    ext = '.' + mime_type.split('/')[-1]
                    new_image_name = f'markdown_{cell_index}_attachment_{i}_{j}{ext}'
                    final_image_fn = self.output_dir / new_image_name
                    b64_bytes = base64.b64decode(base64_data)
                    with open(final_image_fn, 'wb') as f:
                        f.write(b64_bytes)

                    image_dir = self.image_dir_name / new_image_name
                    replace_str = urllib.parse.quote(str(image_dir))
                    cell['source'] = cell['source'].replace(f'attachment:{image_name}', replace_str)
        return cell, resources


class NoExecuteDataFramePreprocessor(Preprocessor):
        
    def preprocess_cell(self, cell, resources, index):
        nb_home = Path(resources['metadata']['path'])
        converter = resources['converter']
        if cell['cell_type'] == 'code':
            outputs = cell.get('outputs', [])
            for output in outputs:
                if 'data' in output:
                    has_image_mimetype = False
                    for key, value in output['data'].items():
                        if key.startswith('image'):
                            has_image_mimetype = True
                            if key == 'image/gif':
                                # gifs not in jinja template
                                key = 'image/png'
                            output['data'] = {key: value}
                            break

                    if not has_image_mimetype and 'text/html' in output['data']:
                        html = output['data']['text/html']
                        if '</table>' in html and '</style>' in html:
                            output['data'] = {'image/png': converter(html)}
                        elif html.startswith('<img src'):
                            pass
                            # maybe necessary if image not embedded with Image(...)
                            # image_files = get_image_tags(html)
                            # if image_files:
                            #     src = nb_home / image_files[0][1]
                            #     ext = str(src).split('.')[-1].split('?')[0]
                            #     data = open(src, 'rb').read()
                            #     data = base64.b64encode(data).decode()
                            #     output['data'] = {f'image/{ext}': data}
        return cell, resources 