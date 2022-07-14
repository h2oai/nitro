
# ## Localization
# Set `mode='toggle'` to show a toggle.
def help_localization(view: View):  # height 4
    glazed, sprinkles, hot = True, False, False
    while True:
        description = f'''
        You want your donut {"glazed" if glazed else "frosted"}, 
        {"with" if sprinkles else "without"} sprinkles, 
        and {"hot" if hot else "warm"}!
        '''
        glazed, sprinkles, hot = view(
            '### Customize my donut!',
            box('Make it glazed', mode='toggle', value=glazed),
            box('Add sprinkles', mode='toggle', value=sprinkles),
            box('Make it hot', mode='toggle', value=hot),
            description,
        )
