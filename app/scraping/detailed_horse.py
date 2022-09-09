from typing import Any, Dict
from bs4 import BeautifulSoup
import re

from horsereality.models import Horse

class DetailedHorse(Horse):
    
    def __init__(self, *, http, data):
        super().__init__(http=http, data=data)

        self.total_gp: int = data.get('total_gp')

        # gp
        self.gp_stats: Dict[str, int] = data.get('gp_stats')

        # discipline gp
        self.discipline_gp: Dict[str, int] = {
            'dressage': self.gp_stats['agility'] + self.gp_stats['balance'] + self.gp_stats['strength'],
            'driving': self.gp_stats['agility'] + self.gp_stats['pulling_power'] + self.gp_stats['speed'] + self.gp_stats['stamina'] + self.gp_stats['strength'],
            'endurance': self.gp_stats['speed'] + self.gp_stats['stamina'] + self.gp_stats['strength'] + self.gp_stats['surefootedness'],
            'eventing': self.gp_stats['balance'] + self.gp_stats['bascule'] + self.gp_stats['speed'] + self.gp_stats['strength'] + self.gp_stats['surefootedness'],
            'flat_racing': self.gp_stats['speed'] + self.gp_stats['acceleration'] + self.gp_stats['stamina'] + self.gp_stats['sprint'],
            'show_jumping': self.gp_stats['acceleration'] + self.gp_stats['agility'] + self.gp_stats['bascule'] + self.gp_stats['sprint'] + self.gp_stats['strength'],
            'western_reining': self.gp_stats['acceleration'] + self.gp_stats['agility'] + self.gp_stats['balance'] + self.gp_stats['surefootedness']
         }

        # confo
        self.confo_stats: Dict[str, str] = data.get('confo_stats')

        self.confo_totals: Dict[str, int] = data.get('confo_totals') # number of "very good", etc

    def to_dict(self) -> Dict[str, Any]:
        base_data = super().to_dict()
       
        detailed_data = {
            'total_gp': self.total_gp,
            'gp_stats': self.gp_stats,
            'discipline_gp': self.discipline_gp,
            'confo_stats': self.confo_stats,
            'confo_totals': self.confo_totals,
        }
        return base_data | detailed_data # merge operator        

    @classmethod
    async def _from_page(cls, client, http, html_text):

        horse = await Horse._from_page(http, html_text)
        data = horse.to_dict()

        # calling to_dict() formats layers differently than how the parent constructor expects it
        data['layers'] = {
            'adult': horse.adult_layers,
            'foal': horse.foal_layers
        }
        
        # gp
        genetic_html = await DetailedHorse._get_horsetab_html(client, 'genetics', horse.lifenumber)
        soup = BeautifulSoup(genetic_html, 'html.parser')
        total_gp = soup.find(string=re.compile('GP total:')).strip()
        # save just the number, bearing in mind it could be up to 1000
        data['total_gp'] = int(total_gp[10:])

        # gp_stats
        # will be acquired similarly to the way the horsereality library gets two-column info about horses in models.py
        gp_stats = {}

        left_info = soup.select('div.genetic_table_row .genetic_potential')
        right_info = soup.select('div.genetic_table_row .genetic_stats')
        for left, right in zip(left_info, right_info):
            key = left.string.strip().lower().replace(' ', '_')
            value = int(right.string.strip())
            gp_stats[key] = value
        data['gp_stats'] = gp_stats

        # confo_stats: just like gp_stats
        confo_html = await DetailedHorse._get_horsetab_html(client, 'achievements', horse.lifenumber)
        soup = BeautifulSoup(confo_html, 'html.parser')
        confo_stats = {}
        confo_totals = {
            'very_good': 0,
            'good': 0,
            'average': 0,
            'below_average': 0,
            'poor': 0
        }

        left_info = soup.select('div.genetic_table_row .genetic_potential')
        right_info = soup.select('div.genetic_table_row .genetic_stats')
        for left, right in zip(left_info, right_info):
            key = left.string.strip().lower().replace(' ', '_')
            value = right.string.strip().lower().replace(' ', '_')
            confo_stats[key] = value
            confo_totals[value] = confo_totals[value] + 1
        data['confo_stats'] = confo_stats
        data['confo_totals'] = confo_totals

        return cls(http=http, data=data)

    # gets the html under the summary, training, genetics, achievements, offspring, health, or update tabs
    @classmethod
    async def _get_horsetab_html(cls, client, tab: str, lifenumber: int):
        post_response = await client.http.request(
            method='POST',
            path='/ajax/update_horsetab.php',
            v2=False,
            data={
                'hid': str(lifenumber),
                'newtab': f'tab_{tab}2'
            },
            headers={'User-Agent': 'Barley\'HorseRealityTools/1.0 (Language=Python/3.10.0)'},
            allow_redirects=False
        )

        return post_response['data']