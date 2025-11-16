#!/bin/bash

# Quick test of PersonaGenerator with mock data

echo "🧪 Testing PersonaGenerator..."
echo ""

# Test persona synthesizer with sample data
echo "📊 Testing persona synthesis module..."
python3 -c "
from persona_synthesizer import PersonaSynthesizer

# Sample profile data
sample_profiles = [
    {
        'name': 'Sarah Chen',
        'headline': 'VP of Engineering at TechCorp | Building scalable AI systems',
        'location': 'San Francisco Bay Area',
        'about': 'Passionate about building high-performing engineering teams and scalable cloud infrastructure. 15+ years experience leading technical organizations.',
        'experience': [
            {'title': 'VP Engineering', 'company': 'TechCorp', 'duration': '2020 - Present'},
            {'title': 'Director of Engineering', 'company': 'StartupXYZ', 'duration': '2017 - 2020'},
            {'title': 'Senior Engineering Manager', 'company': 'BigTech Inc', 'duration': '2014 - 2017'},
        ],
        'education': [
            {'school': 'Stanford University', 'degree': 'MS Computer Science'},
            {'school': 'UC Berkeley', 'degree': 'BS Computer Science'},
        ],
        'skills': ['Leadership', 'Cloud Architecture', 'Python', 'Team Building', 'Agile', 'Kubernetes'],
        'posts': [
            {'text': 'Excited to share our journey migrating to microservices. Key lessons learned about team autonomy and technical debt...'},
            {'text': 'Hiring great engineering talent is harder than ever. Here are 5 strategies that worked for us...'},
        ]
    },
    {
        'name': 'Michael Rodriguez',
        'headline': 'CTO | Technical Co-founder | Ex-Amazon',
        'location': 'Seattle, WA',
        'about': 'Building the future of e-commerce infrastructure. Former Principal Engineer at Amazon. Angel investor in early-stage startups.',
        'experience': [
            {'title': 'CTO & Co-founder', 'company': 'ShopTech', 'duration': '2021 - Present'},
            {'title': 'Principal Engineer', 'company': 'Amazon', 'duration': '2016 - 2021'},
            {'title': 'Senior Software Engineer', 'company': 'Microsoft', 'duration': '2012 - 2016'},
        ],
        'education': [
            {'school': 'MIT', 'degree': 'MS Electrical Engineering'},
            {'school': 'University of Washington', 'degree': 'BS Computer Engineering'},
        ],
        'skills': ['System Design', 'AWS', 'Distributed Systems', 'Go', 'Leadership', 'Product Strategy'],
        'posts': [
            {'text': 'The biggest mistake technical founders make is not thinking about scalability from day one...'},
            {'text': 'Just closed our Series A! Incredibly grateful to our team and investors who believed in our vision...'},
        ]
    },
    {
        'name': 'Jennifer Kim',
        'headline': 'Head of Engineering | Building Developer Tools',
        'location': 'New York, NY',
        'about': 'Developer tools enthusiast. Previously led engineering teams at Stripe and GitHub. Passionate about developer experience and open source.',
        'experience': [
            {'title': 'Head of Engineering', 'company': 'DevTools Co', 'duration': '2022 - Present'},
            {'title': 'Engineering Manager', 'company': 'Stripe', 'duration': '2019 - 2022'},
            {'title': 'Senior Engineer', 'company': 'GitHub', 'duration': '2016 - 2019'},
        ],
        'education': [
            {'school': 'Carnegie Mellon University', 'degree': 'BS Computer Science'},
        ],
        'skills': ['Developer Tools', 'APIs', 'TypeScript', 'Engineering Management', 'Open Source', 'CI/CD'],
        'posts': [
            {'text': 'Great developer experience is not about the tools you build, but about the problems you solve...'},
            {'text': 'Hiring engineers who care about craft AND impact is the ultimate unlock for any devtools company...'},
        ]
    }
]

print('✅ Sample profiles loaded')
print(f'📊 Processing {len(sample_profiles)} profiles...')
print('')

synthesizer = PersonaSynthesizer(model='qwen')
persona = synthesizer.synthesize_persona(sample_profiles, 'Tech_Executive_Test')

print('')
print('✅ Persona generated!')
print('')
print('Preview (first 1000 chars):')
print('─' * 60)
print(persona[:1000])
print('...')
print('─' * 60)

# Save to file
import os
os.makedirs('output', exist_ok=True)
with open('output/test_persona.md', 'w') as f:
    f.write(persona)

print('')
print('💾 Full persona saved to: output/test_persona.md')
print('')
print('✨ Test complete! PersonaGenerator is working.')
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Test Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "View the generated persona:"
echo "cat output/test_persona.md"
echo ""
