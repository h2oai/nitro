from datetime import datetime, timedelta
from h2o_nitro import AsyncView as View, box, option, row, col


# The job application workflow. Spans seven pages.
async def main(view: View):
    await view('''
    # Want to be an astronaut?
    
    Maybe you've seen astronauts working on the International Space Station, or heard about our plans to send humans 
    back to the Moon or maybe you've been following the ongoing exploration of Mars and want to visit the planet for 
    yourself one day! 
    
    Whatever your inspiration has been, you know you want to become an astronaut. 
    So how do you get there, and what can you do to make it possible?
    
    #### You've come to the right place. Let's start your application.
    ''')

    position = await view(
        '''
        # What kind of position are you applying for?
        
        Choose an option that best suits your situation. 
        ''',
        box([
            option('full-time', 'Full time', caption="I'm a seasoned pro. To the galaxy and beyond!", selected=True),
            option('internship', 'Internship', caption="I'm still learning and want to explore opportunities"),
        ])
    )

    name, phone, email, region, preference = await view(
        '''
        # How do we contact you?
        
        We prefer to reach you by phone, but an email address is OK, too. 
        ''',
        box('Full name', placeholder='Boaty McBoatface'),
        row(
            box('Phone', mask='(999) 999 - 9999'),
            box('Email', placeholder='you@company.com', icon='Mail'),
        ),
        box('Region', mode='menu', options=[
            'Africa', 'Asia', 'Australia', 'Europe', 'North America', 'South America',
        ]),
        box('Reach me:', mode='radio', options=[
            option('any', 'Any time.', selected=True),
            option('work', 'Only between 9am and 5pm.'),
        ])
    )

    job_code, experience, interests = await view(
        '''
        # What are your skills and interests?
        
        Help us find you the best position that aligns with your goals.
        ''',
        box('I want to be a:', mode='radio', options=[
            option('pilot', 'Pilot', icon='Airplane'),
            option('mission_spl', 'Mission Specialist', icon='CalendarSettings'),
            option('flight_eng', 'Flight Engineer', icon='Settings'),
            option('payload_spl', 'Payload Specialist', icon='PlugDisconnected'),
            option('dj', 'Resident DJ', icon='MusicInCollection'),
        ]),
        row(
            col(box('I have experience with:', mode='check', options=[
                'Living in space',
                'Manufacturing',
                'Robotics',
                'Instrumentation',
                'High-tech computing',
            ])),
            col(box('I am interested in:', mode='check', options=[
                'Commercial Crew',
                'Space Telescopes',
                'The Jupiter Mission',
                'The Mars Rover',
                'The Solar Probe',
                'International Space Station',
            ]))
        ),
    )

    link, bio = await view(
        '''
        # Almost Done!
        
        Thank you for taking the time to fill out this application. 
        
        If there's anything else you'd like us to know, let us know. 
        ''',
        box('Resume or website', prefix='https://'),
        box(placeholder='Anything about me, qualifications, accomplishments, or relevant information.', lines=10),
    )

    referral, communication = await view(
        '''
        # How did you hear about us?

        You don't have to tell us, but it'll help our statisticians. 
        ''',
        box(placeholder='Heard about you on the news.', lines=5),

        box(mode='check', options=[
            option('share', 'Share this with everyone.', selected=True),
            option('email', 'Subscribe me to 10 emails a day!', selected=True),
        ])
    )

    await view(
        f'''
        # Thank you!
        
        Your application is being reviewed. We'll be in touch shortly.
        
        ## Summary
        
        ### Details
        
        - Position: {position} 
        - Name: {name}
        - Phone: {phone}
        - Email: {email}
        - Region: {region}
        - Preference: Contact me {'during work hours' if preference == 'work' else 'any time'}.
        - Job Code: `{job_code}` 
        - Experience; {', '.join(experience)}
        - Interests: {', '.join(interests)}
        - Link: {link}
        
        ### Bio
        
        {bio}
        
        ### How did you hear about us?
        
        {referral}
        
        ### Other
        
        - {'Share my info' if 'share' in communication else "Don't share my info"}.
        - {'Send me emails' if 'email' in communication else "Don't send me emails"}.
        
        '''
    )


# A shorter workflow. Spans two pages.
async def contact(view: View):
    name, phone, date, preference = await view(
        '''
        # Have a question?
        
        Let us know how to reach you, and we'll get in touch.
        ''',
        box('Full name', placeholder='Boaty McBoatface'),
        box('Phone', mask='(999) 999 - 9999'),
        # Allow at least a week from now.
        box('Call me on', mode='date', min=(datetime.now() + timedelta(weeks=1)).isoformat()[:10]),
        box('Reach me:', mode='radio', options=[
            option('any', 'Any time.', selected=True),
            option('work', 'Only between 9am and 5pm.'),
        ]),
    )

    await view(
        f'''
        # Thank you for reaching out, {name}!
        
        We will contact you at {phone} on {date}{' during work hours' if preference == 'work' else ''}.
        '''
    )


# A simple page that links to other pages.
async def about(view: View):
    choice = view('''
    # About
    
    > "The world we have created is a product of our thinking;
    > it cannot be changed without changing our thinking." 
    > *— Albert Einstein*
    
    We are organizing the planet's first Space Program, where astronauts, from any walk of life, can apply for an 
    opportunity to travel to space and experience the galaxy far, far away, and beyond.
    
    [Apply now](#apply).
    
    [Have a question?](#question)
    ''')

    if choice == 'apply':
        await main(view)
    elif choice == 'question':
        await contact(view)


nitro = View(
    main,
    # The app's title and caption, displayed at tht top.
    title='Hello Astronaut!',
    caption='Apply for space travel',
    # The main menu, displayed at the top left.
    menu=[
        option(main, 'Apply'),
        option(contact, 'Contact Us'),
        option(''),  # menu separator
        option(about, 'About'),
    ],
    # The navigation bar, displayed at the top right.
    nav=[
        option(about, 'About'),
    ])
