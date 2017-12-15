from django.db import models

# Create your models here.
class table_basic(models.Model):
    table_name = models.CharField(max_length=255)
    table_columns = models.IntegerField()
    table_rows = models.IntegerField()
    update_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.table_name

class table_content(models.Model):
    table_id = models.IntegerField()
    cell_column = models.IntegerField()
    cell_row = models.IntegerField()
    cell_content = models.CharField(max_length=1000)
    def __unicode__(self):
        return self.cell_content

class table_head(models.Model):
    table_id = models.IntegerField()
    head_column = models.IntegerField()
    head_content = models.CharField(max_length=50)
    def __unicode__(self):
        return self.head_content
