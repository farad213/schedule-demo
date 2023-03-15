from django.db import models

class BuildingsGMO(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"GMO -{self.sorszam} - {self.szerkezeti_hossz}"

class BuildingsGKB(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"GKB - {self.sorszam} - {self.szerkezeti_hossz}"

class BuildingsGU(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"GU - {self.sorszam} - {self.szerkezeti_hossz}"

class BuildingsGEM(models.Model):
    sorszam = models.IntegerField()
    szerkezeti_hossz = models.FloatField()

    def __str__(self):
        return f"GEM - {self.sorszam} - {self.szerkezeti_hossz}"

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


class Technician(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    position_HU = models.CharField(max_length=50)
    position_EN = models.CharField(max_length=50)
    signature = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    position_HU = models.CharField(max_length=50)
    position_EN = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)

    def __str__(self):
        return self.name