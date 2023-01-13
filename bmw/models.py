from django.db import models

class BuildingsTMO(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"TMO -{self.sorszam} - {self.szerkezeti_hossz}"

class BuildingsTKB(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"TKB - {self.sorszam} - {self.szerkezeti_hossz}"

class BuildingsTU(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"TU - {self.sorszam} - {self.szerkezeti_hossz}"

class BuildingsTEM(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"TEM - {self.sorszam} - {self.szerkezeti_hossz}"

class JelkodCCS(models.Model):
    notation = models.CharField(max_length=5)
    length = models.FloatField()

    def __str__(self):
        return f"{self.notation} - {self.length}"

class JelkodVVS(models.Model):
    notation = models.CharField(max_length=5)
    length = models.FloatField()

    def __str__(self):
        return f"{self.notation} - {self.length}"