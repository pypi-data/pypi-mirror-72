from wagtail.core import blocks

from webspace.cms.blocks.choice import AlignTextChoiceBlock
from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    SvgWithSizeBlock, \
    ImageWithSizeBlock, \
    ButtonBlock, \
    EntryBlock, \
    EmbedWithSizeBlock, \
    FormBlock


class ComponentTextEntry(EntryBlock):
    amp_scripts = ['iframe', 'form']
    titles = TextBlock(label="Titres")
    text = TextBlock(label="Description")
    reverse = blocks.BooleanBlock(required=False, help_text="Permet de d'intervertir le component et la zone de texte")
    section = blocks.BooleanBlock(required=False, help_text="Permet de sectionner la zone de texte")
    align = AlignTextChoiceBlock(required=False)
    component = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
            ('embed', EmbedWithSizeBlock()),
            ('form', FormBlock()),
        ],
        max_num=1,
        required=False
    )
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=2, required=False
    )

    def mock(self, component='svg', align=None,
             section=False, reverse=False, size_component='m', button_1=constants.BUTTON_PRIMARY_FULL, button_2=None,
             *args, **kwargs):
        if component == 'svg':
            if 'theme' in kwargs:
                file = self.mocker.SVG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT else self.mocker.SVG_SQUARE_SPACE
            else:
                file = self.mocker.SVG_SQUARE_SPACE
        else:
            if 'theme' in kwargs:
                file = self.mocker.IMG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT else self.mocker.IMG_SQUARE_SPACE
            else:
                file = self.mocker.IMG_SQUARE_SPACE
        ret = {
            'type': 'component_text',
            'value': {
                'titles': {'value': self.mocker.h1},
                'text': {
                    'value': self.mocker.normal
                },
                'component': [{
                    'type': component,
                    'value': {
                        'file': self.mocker.file(file).id,
                        'size': size_component
                    },
                }],
                'buttons': [],
                'reverse': reverse,
                'align': align,
                'section': section
            }
        }
        if component == 'embed':
            ret['value']['component'] = [{
                'type': 'embed',
                'value': {
                    'link': self.mocker.URL_EMBED,
                    'size': size_component
                }
            }]
        if component == 'form':
            form = self.mocker.get_form('small', 2, head_text=False)
            ret['value']['component'] = [{
                'type': 'form',
                'value': {
                    'form': form.id,
                }
            }]
        if button_1:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': self.mocker.button(button_1)
            })
        if button_2:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': self.mocker.button(m_type=button_2)
            })
        self.mock_data.update(ret)
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/component_text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Component Text"
