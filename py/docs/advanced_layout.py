# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from h2o_nitro import View, box, row, col, option, lorem


# # Advanced

# ## Embedding Web Pages
# Set `mode='web'` to embed external web pages.
def embed_iframe(view: View):
    view(box(mode='web', path='https://example.com'))


# ## An Album
# A simple layout for photo galleries or portfolios.
#
# Inspired by the [Bootstrap Album](https://getbootstrap.com/docs/4.0/examples/album/).
def layout_album(view: View):  # height 11
    cards = [make_album_card(lorem(1), i) for i in range(9)]

    view(
        col(
            box(f'## {lorem()}\n\n{lorem(3)}', align='center'),
            box(dict(yes='Primary', no='Secondary'), align='center'),
            color='$background', background='$foreground',
            padding='8rem', tile='center',
        ),
        row(
            *cards,
            background='$neutral-lighter',
            wrap='between', tile='center', padding='3rem'
        ),
        gap=0,
    )


def make_album_card(text, views):
    return col(
        box(image='image.png', height=200),
        box(text, padding='0 1rem'),
        row(
            box(mode='button', options=[
                option('view', 'View', selected=False, options=[
                    option('edit', 'Edit', icon='Edit')
                ])
            ]),
            box(f'{views + 1} views', align='right', color='$neutral-secondary'),
            padding='1rem', tile='between', cross_tile='end',
        ),
        background='$background', border='$neutral-tertiary-alt',
        padding=0, width='32%',
    )
