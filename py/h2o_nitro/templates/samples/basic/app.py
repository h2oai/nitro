from h2o_nitro import AsyncView as View, box


async def main(view: View):
    name = await view(box('What is your name?', value='Boaty McBoatface'))
    feel = await view(box(f'How do you feel today, {name}?', value='intrigued'))
    await view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')
