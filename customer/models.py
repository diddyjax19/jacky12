from itertools import combinations

from django.db import models
from django.db.models import Q


class Table(models.Model):
    size = models.PositiveIntegerField()

    def __str__(self):
        return str(self.size)


class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    tables = models.ManyToManyField(Table)

    @staticmethod
    def optimise(smaller_tables, bigger_tables, party):

        if smaller_tables:
            for combination in combinations(smaller_tables, 2):
                if sum([table.size for table in combination]) == party:
                    return list(combination)

        if bigger_tables:
            bigger_tables.sort(key=lambda x: x.size)

            return list(bigger_tables[:1])

    def find_table(self, date, time, end_time, party, optimise=False):

        tables = self.tables.all()

        available_tables = []

        for table in tables:

            if table.booking_set.filter(
                    Q(date=date, time__range=(time, end_time)) | Q(date=date, end_time__range=(time, end_time))):

                continue
            else:
                available_tables.append(table)

        smaller_tables = []

        bigger_tables = []

        for table in available_tables:
            if table.size == party:
                return [table]  # Great this is perfectly sized, use it.
            elif table.size < party:
                smaller_tables.append(table)
            else:
                bigger_tables.append(table)
        else:
            if optimise:
                return self.optimise(smaller_tables, bigger_tables, party)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ReservationOrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    noOfSeatReserved = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)

#

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'

#
# class Booking(models.Model):
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     party_size = models.PositiveIntegerField()
#     table = models.ManyToManyField(Table)
#     date = models.DateField()
#     time = models.TimeField()
#     length = models.DurationField()
#     end_time = models.TimeField()
#
#     def __str__(self):
#         return 'Booking for {party} at {restaurant} on {date}'.format(party=self.party_size,
#                                                                       restaurant=self.restaurant,
#                                                                       date=self.time)
