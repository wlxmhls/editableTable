# -*- coding: utf-8 -*-
import os
import time

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators import csrf
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

from cmdb.models import table_basic, table_content, table_head

TABLEINDEX = os.getcwd() + "/templates/index.html"


def table(request):
    return tablegenerate(request)


def tablenewform(request):
    return render(request, "tablenewform.html")

def tablegenerate(request):
    request.encoding = 'utf-8'

    ctx = {}
    indexfile = open(TABLEINDEX, "r")
    indexcontent = indexfile.read()
    indexfile.close()

    alltables = table_basic.objects.raw("select * from cmdb_table_basic order by update_time desc")

    for eachtable in alltables:
        ctx["table_name"] = eachtable.table_name
        ctx["table_cols"] = eachtable.table_columns
        ctx["table_rows"] = eachtable.table_rows

        table_id = str(eachtable.id)
        query = 'select * from cmdb_table_head where table_id=' + table_id + ' order by head_column'
        allheads = table_head.objects.raw(query)

        query = 'select * from cmdb_table_content where table_id=' + table_id + ' order by cell_row, cell_column'
        allcells = table_content.objects.raw(query)

        context = {'ctx':ctx, 'cols_range':range(0,int(ctx["table_cols"])), 'rows_range':range(0,int(ctx["table_rows"])), 'hide':1, 'allheads':allheads, 'allcells':allcells}
        tablefrmcontent = render_to_string("tableframe.html", context)

        indexpos = indexcontent.find('<label name="add new table before"></label>')
        if indexpos != -1:
            indexcontent = indexcontent[:indexpos] + tablefrmcontent + indexcontent[indexpos:]

    return HttpResponse(indexcontent)


def cellupdate(request):
    request.encoding = 'utf-8'

    if request.POST:
        table_name = request.POST["tabname"]
        table_id = table_basic.objects.filter(table_name=table_name)[0].id
        cell_type = request.POST["type"]
        cell_col = request.POST["col"]
        cell_row = request.POST["row"]
        cell_content = request.POST["cellcontent"].strip()

        if cell_type == "head":
            table_head.objects.filter(table_id=table_id).filter(head_column=cell_col).update(head_content=cell_content)
        else:
            table_content.objects.filter(table_id=table_id).filter(cell_column=cell_col).filter(cell_row=cell_row).update(cell_content=cell_content)

        date_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        table_basic.objects.filter(id=table_id).update(update_time=date_time)

    return HttpResponse('cell updated')


def celladd(request):
    request.encoding = 'utf-8'
    add_type = ''

    if request.POST:
        table_name = request.POST["tabname"]
        table_id = table_basic.objects.filter(table_name=table_name)[0].id
        cell_type = request.POST["type"]
        cell_col = request.POST["col"]
        cell_row = request.POST["row"]
        cell_content = request.POST["cellcontent"].strip()
        add_type = request.POST["addtype"]

        if cell_type == "head":
            table_info = table_basic.objects.get(id=table_id)
            table_info.table_columns += 1
            table_info.save()

            table_head(table_id=table_id, head_column=cell_col, head_content=cell_content).save()
        else:
            if add_type== "row":
                table_info = table_basic.objects.get(id=table_id)
                table_info.table_rows += 1
                table_info.save()
            else:
                table_content(table_id=table_id, cell_column=cell_col, cell_row=cell_row, cell_content=cell_content).save()

    return HttpResponse('cell added')


def celldel(request):
    request.encoding = 'utf-8'
    del_type = ''

    if request.POST:
        table_name = request.POST["tabname"]
        table_id = table_basic.objects.filter(table_name=table_name)[0].id
        cell_type = request.POST["type"]
        cell_col = request.POST["col"]
        cell_row = request.POST["row"]
        del_type = request.POST["deltype"]

        if cell_type == "head":
            table_head.objects.filter(table_id=table_id).filter(head_column=cell_col).delete()

            table_info = table_basic.objects.get(id=table_id)
            table_info.table_columns -= 1
            table_info.save()

            query = "select * from cmdb_table_head where table_id=" + str(table_id) + " and head_column>" + str(cell_col)
            updatedcols = table_head.objects.raw(query)

            for col in updatedcols:
                col.head_column -= 1
                col.save()

        else:
            if del_type == 'row':
                table_info = table_basic.objects.get(id=table_id)
                table_info.table_rows -= 1
                table_info.save()

            table_content.objects.filter(table_id=table_id).filter(cell_column=cell_col).filter(cell_row=cell_row).delete()

            if del_type == 'column':
                query = "select * from cmdb_table_content where table_id=" + str(table_id) + " and cell_row=" + str(cell_row) + " and cell_column>" + str(cell_col)
                updatedcols = table_content.objects.raw(query)

                for col in updatedcols:
                    col.cell_column -= 1
                    col.save()

            if del_type == 'rowcell':
                query = "select * from cmdb_table_content where table_id=" + str(table_id) + " and cell_row>" + str(cell_row) + " and cell_column=" + str(cell_col)
                updatedrows = table_content.objects.raw(query)

                for row in updatedrows:
                    row.cell_row -= 1
                    row.save()

    return HttpResponse('cell deleted')


def tableclr(request):
    request.encoding = 'utf-8'

    if 'tabname' in request.GET:
        try:
            tableid = table_basic.objects.get(table_name=request.GET['tabname']).id
        except:
            return HttpResponse(u'<h3>'+request.GET['tabname']+u'表不存在</h3>')

        table_basic.objects.filter(id=tableid).update(table_rows=0)
        table_content.objects.filter(table_id=tableid).delete()


def tabledel(request):
    request.encoding = 'utf-8'

    if 'tabname' in request.GET:
        try:
            tableid = table_basic.objects.get(table_name=request.GET['tabname']).id
        except:
            return HttpResponse(u'<h3>'+request.GET['tabname']+u'表不存在</h3>')

        table_basic.objects.filter(table_name=request.GET['tabname']).delete()
        table_head.objects.filter(table_id=tableid).delete()
        table_content.objects.filter(table_id=tableid).delete()

    return render(request, "index.html")


def tablenew(request):
    request.encoding='utf-8'

    ctx = {}
    if request.POST:
        ctx["table_name"] = request.POST["table_name"]
        ctx["table_cols"] = request.POST["table_cols"]
        ctx["table_rows"] = request.POST["table_rows"]

        context = {'ctx':ctx, 'cols_range':range(0,int(ctx["table_cols"])), 'rows_range':range(0,int(ctx["table_rows"])), 'hide':0, 'allheads':0, 'allcells':0}
        tablefrmcontent = render_to_string("tableframe.html", context)
        indexfile = open(TABLEINDEX, "r")
        indexcontent = indexfile.read()
        indexfile.close()

        indexpos = indexcontent.find('<label name="add new table before"></label>')
        if indexpos != -1:
            indexcontent = indexcontent[:indexpos] + tablefrmcontent + indexcontent[indexpos:]

        newtable = table_basic(table_name=ctx["table_name"], table_columns=ctx["table_cols"], table_rows=ctx["table_rows"])
        newtable.save()
        for col in range(1, int(ctx["table_cols"])+1):
            newtablehead = table_head(table_id=newtable.id, head_column=col, head_content='列'+str(col))
            newtablehead.save()

            for row in range(1, int(ctx["table_rows"])+1):
               newtablecontent = table_content(table_id=newtable.id, cell_column=col, cell_row=row, cell_content='')
               newtablecontent.save()

        return HttpResponse(indexcontent)

    else:
        return render(request, "index.html")


def useradd(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'useradd.html', context={'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', context={'form': form})
