import sqlite3

CONN = sqlite3.connect ("dogs.db")

CURSOR = CONN.cursor()
from .dog import Dog