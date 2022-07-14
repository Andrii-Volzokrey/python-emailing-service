from main.mail_instance import Mail
from main.utils import set_up_template
from presets.replacements import base_replacements
from main.images.example_img.data import data as example_image_src_data


replacements_for_example = {
    'example_img': example_image_src_data['url'] if example_image_src_data['url'] else example_image_src_data['cid']
}


def example_mail_preset(from_mail, to_mail, replacements):
    template = set_up_template(
        'example.html',
        {**base_replacements, **replacements, **replacements_for_example}
    )

    mail = Mail(
        from_mail,
        to_mail,
        'Example Preset Subject',
        template,
    )

    if not example_image_src_data['url']:
        mail.attach_image(example_image_src_data['path'], cid=example_image_src_data['raw_cid'])

    return mail
