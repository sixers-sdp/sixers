from django.core.management.base import BaseCommand, CommandError
import json
import requests



# grab access token from ask-cli
from main.models import ProductCategory, Product

BASE_ADDRESS = 'https://api.amazonalexa.com'

SKILL_ID = 'amzn1.ask.skill.74c15662-c671-4545-adfe-fe2be939a930'
SKILL_URL = f'{BASE_ADDRESS}/v1/skills/{SKILL_ID}/stages/development/interactionModel/locales/en-GB'
with open('/home/visgean/.ask/cli_config') as f:
    cli_data = json.loads(f.read())

access_token = cli_data['profiles']['default']['token']['access_token']

headers = {
    'Authorization': access_token
}


MENUS_TO_IMPORT = [
    'Menu', 'Drink'
]


class Command(BaseCommand):
    help = 'Imports menu from the Alexa skill'

    def handle(self, *args, **options):
        r = requests.get(SKILL_URL, headers=headers)
        r.raise_for_status()

        model = r.json()

        menus = model['interactionModel']['languageModel']['types']

        for menu in menus:
            if menu['name'] not in MENUS_TO_IMPORT:
                continue

            category, _= ProductCategory.objects.get_or_create(name=menu['name'])

            print(menu['name'])
            for product in menu['values']:
                name = product['name']['value']
                synonyms = product['name'].get('synonyms', [])
                synonyms_str = ','.join(synonyms)

                if 'id' in product and Product.objects.filter(id=product['id']).exists():
                    obj = Product.objects.get(id=product['id'])
                    obj.name = name
                    obj.synonyms = synonyms_str
                    obj.save()
                else:
                    Product(
                        name=name,
                        synonyms=synonyms_str,
                        category=category,
                        price=0
                    ).save()

                print('  -', product['name']['value'])
