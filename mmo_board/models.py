from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader import fields


class Category(models.Model):

    tank = 'TK'
    heal = 'HL'
    damage_dealer = 'DD'
    trader = 'TR'
    guild_master = 'GM'
    quest_giver = 'QG'
    blacksmith = 'BS'
    tanner = 'LS'
    potion_crafter = 'BC'
    spell_master = 'SM'

    CATEGORIES = [
        (tank, 'Tank'),
        (heal, 'Healer'),
        (damage_dealer, 'DD'),
        (trader, 'Trader'),
        (guild_master, 'Guildmaster'),
        (quest_giver, 'Questgiver'),
        (blacksmith, 'Blacksmith'),
        (tanner, 'Leathersmith'),
        (potion_crafter, 'Potioncrafter'),
        (spell_master, 'Spellmaster'),

    ]

    name = models.CharField(max_length=2, choices=CATEGORIES)

    def __str__(self):
        for value in self.CATEGORIES:
            if self.name == value[0]:
                return value[1]


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    category = models.ManyToManyField(to='Category')
    date_created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = fields.RichTextUploadingField()


class Response(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    text = models.TextField()
    approved = models.BooleanField(default=False)




