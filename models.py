from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Optional


class Prize(models.Model):
    """
    Модель приза
    """
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=50, null=True)


class Participant(models.Model):
    """
    Модель участника
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)

    def category_description(self) -> str:
        """
        Returns category description
        """
        for category in categories:
            if category['id'] == self.category_id:
                return category['description']
        return ''


class Users(models.Model):
    """
    Модель участника
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)

    def category_description(self) -> str:
        """
        Returns category description
        """
        for category in categories:
            if category['id'] == self.category_id:
                return category['description']
        return ''


class Promo(models.Model):
    """
    Модель промоакции
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    description: Optional[str] = fields.CharField(max_length=50, null=True)
    participants: list
    prizes: list


class Result(models.Model):
    winner: Participant
    prize: Prize


Participant_Pydantic = pydantic_model_creator(Participant, name="Participant")
ParticipantIn_Pydantic = pydantic_model_creator(Participant, name="ParticipantIn", exclude_readonly=True)

Promo_Pydantic = pydantic_model_creator(Promo, name="Promo")
PromoIn_Pydantic = pydantic_model_creator(Promo, name="PromoIn", exclude_readonly=True)

User_Pydantic = pydantic_model_creator(Participant, name="User")
UserIn_Pydantic = pydantic_model_creator(Participant, name="UserIn", exclude_readonly=True)
