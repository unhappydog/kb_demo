from flask import Blueprint
inf_restful = Blueprint('inf_restful', __name__)
from . import Views, LinkingViews, DataViews, TalentBankViews, TalentBankViewsV2, UserViews, KBViews
