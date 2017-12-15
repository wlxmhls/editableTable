var csrftoken = $.cookie('csrftoken');

// Set element double click editable
function SetEditable(Ele) {
    $(Ele).dblclick(function (e) {
        e.stopPropagation();
        $(this).attr('contenteditable','true');
        $(this).blur(function(){
            $(this).attr('contenteditable','false');
            rowno = this.parentNode.rowIndex - 1;
            colno = this.cellIndex;
            tabname = this.parentNode.parentNode.parentNode.parentNode.parentNode.getElementsByTagName('a')[0].innerText;
            cellcontent = this.innerText;

            if (rowno == 0) {
                $.ajax({
                    type: 'POST',
                    url: '/cellupdate',
                    data: {
                        tabname: tabname,
                        type: 'head',
                        col: colno,
                        row: rowno,
                        cellcontent: cellcontent,
                        csrfmiddlewaretoken: csrftoken,
                    },
                });
            }
            else {
                $.ajax({
                    type: 'POST',
                    url: '/cellupdate',
                    data: {
                        tabname: tabname,
                        type: 'cell',
                        col: colno,
                        row: rowno,
                        cellcontent: cellcontent,
                        csrfmiddlewaretoken: csrftoken,
                    },
                });
            }
        });

        $(this).focus();
    });
}

//Add a new column
function AddNewColumn(btn) {
    var tab = btn.parentNode.getElementsByTagName('table')[0];
    var tabname = tab.parentNode.parentNode.getElementsByTagName('a')[0].innerText;
    var rowLength = tab.rows.length;
    var newcolumnID = tab.rows[1].cells.length - 1;
 
    for (var i = 0; i < rowLength; i++) {
        var oTd = tab.rows[i].insertCell(newcolumnID);
        var rowno = i - 1;

        if (i == 0) {
            oTd.innerHTML = "<a href='#' onclick='DeleteColumn(this)'>删除</a>";

        } else if (i == 1) {
            oTd.innerHTML = '列' + newcolumnID;
            if (newcolumnID > 2) {
                $(tab.rows[i].cells[newcolumnID-1]).resizable();
                SetEditable(tab.rows[i].cells[newcolumnID]);
            }

            $.ajax({
                type: 'POST',
                url: '/celladd',
                data: {
                        tabname: tabname,
                        type: 'head',
                        col: newcolumnID,
                        row: rowno,
                        cellcontent: '列'+newcolumnID,
                        addtype: 'col',
                        csrfmiddlewaretoken: csrftoken,
                },
            });

        } else if (i > 1) {
            oTd.id = 'column' + newcolumnID;
            oTd.innerHTML = '';
            if (newcolumnID > 2) {
                $(tab.rows[i].cells[newcolumnID-1]).resizable();
                SetEditable(tab.rows[i].cells[newcolumnID]);
            }

            $.ajax({
                type: 'POST',
                url: '/celladd',
                data: {
                        tabname: tabname,
                        type: 'cell',
                        col: newcolumnID,
                        row: rowno,
                        cellcontent: '',
                        addtype: 'col',
                        csrfmiddlewaretoken: csrftoken,
                },
            });

        }
    }
}
 
//Delete a column
function DeleteColumn(atag) {
    var tab = atag.parentNode.parentNode.parentNode;
    var tabname = tab.parentNode.parentNode.parentNode.getElementsByTagName('a')[0].innerText;
    var columnId = atag.parentNode.cellIndex;
 
    for (var i = 0; i < tab.rows.length; i++) {
        tab.rows[i].deleteCell(columnId);

        rowno = i - 1;
        //head
        if (i == 1) {
            $.ajax({
                type: 'POST',
                url: '/celldel',
                data: {
                    tabname: tabname,
                    type: 'head',
                    col: columnId,
                    row: rowno,
                    deltype: 'column',
                    csrfmiddlewaretoken: csrftoken,
                },
            });
        }
        //cell
        else if (i > 1) {
            $.ajax({
                type: 'POST',
                url: '/celldel',
                data: {
                    tabname: tabname,
                    type: 'cell',
                    col: columnId,
                    row: rowno,
                    deltype: 'column',
                    csrfmiddlewaretoken: csrftoken,
                },
            });
        }
    }
 
    var lastcol = tab.rows[1].cells.length - 2;
    for (i = 0; i < tab.rows.length; i++) {
        $(tab.rows[i].cells[lastcol]).resizable({disabled: true});
        $(tab.rows[i].cells[lastcol]).resizable('destroy');
    }
}
 
//Add a new row
function AddNewRow(btn) {
    var tab = btn.parentNode.getElementsByTagName('table')[0];
    var tabname = tab.parentNode.parentNode.parentNode.getElementsByTagName('a')[0].innerText;
    var lastcol = tab.rows[1].cells.length - 1;
    var newrowID = tab.rows.length - 1;
    var newTR = tab.insertRow(tab.rows.length);

    for (var i = 0; i < lastcol; i++) {
        if (i == 0) {
            newTR.insertCell(0).innerHTML = newrowID;
            newTR.cells[0].className = 'left';

            $.ajax({
                type: 'POST',
                url: '/celladd',
                data: {
                        tabname: tabname,
                        type: 'cell',
                        col: i,
                        row: newrowID,
                        cellcontent: '',
                        addtype: 'row',
                        csrfmiddlewaretoken: csrftoken,
                },
            });

        } else {
            newTR.insertCell(i).innerHTML = '';
            if (i != lastcol-1)
              $(newTR.cells[i]).resizable();

            SetEditable(newTR.cells[i]);

            $.ajax({
                type: 'POST',
                url: '/celladd',
                data: {
                        tabname: tabname,
                        type: 'cell',
                        col: i,
                        row: newrowID,
                        cellcontent: '',
                        addtype: '',
                        csrfmiddlewaretoken: csrftoken,
                },
            });
        }
    }

    var lastTd = newTR.insertCell(lastcol);
    lastTd.innerHTML = "<a href='#' onclick='DeleteRow(this)'>删除</a>";
    lastTd.className = 'right';
}
 
//Delete a row
function DeleteRow(atag) {
    var tab = atag.parentNode.parentNode.parentNode;
    var tabname = tab.parentNode.parentNode.parentNode.getElementsByTagName('a')[0].innerText;
    var rowtr = atag.parentNode.parentNode;
    var rowIndex = rowtr.rowIndex;
    var rowno = rowIndex - 1;

    tab.deleteRow(rowIndex);

    for (i = 2; i < tab.rows.length; i++) {
        tab.rows[i].cells[0].innerHTML = i - 1;
    }

    for (i = 0; i < tab.rows[1].cells.length-1; i++) {

        if (i == 0) {
            $.ajax({
                type: 'POST',
                url: '/celldel',
                data: {
                    tabname: tabname,
                    type: 'cell',
                    col: i,
                    row: rowno,
                    deltype: 'row',
                    csrfmiddlewaretoken: csrftoken,
                },
            });
        }
        else {
            $.ajax({
                type: 'POST',
                url: '/celldel',
                data: {
                    tabname: tabname,
                    type: 'cell',
                    col: i,
                    row: rowno,
                    deltype: 'rowcell',
                    csrfmiddlewaretoken: csrftoken,
                },
            });
        }
    }
}
 
//Truncate table
function ClearTable(btn) {
    if (confirm('表中所有数据将被删除，确定要清空表吗？')) {
        var tab = btn.parentNode.getElementsByTagName('table')[0];
        var rowscount = tab.rows.length;

        var tabdiv = btn.parentNode.parentNode;
        var tabname = tabdiv.getElementsByTagName('a')[0].innerText;

        //remove rows from tail to head
        for (var i = rowscount-1; i > 1; i--) {
            tab.deleteRow(i);
        }

        $.ajax({
            type: 'GET',
            url: '/tableclr?tabname='+tabname,
        });
    }
}

//Delete table
function DeleteTable(btn) {
    if (confirm('表及其数据将被删除，确定吗？')) {
        var tabdiv = btn.parentNode.parentNode;
        var tabname = tabdiv.getElementsByTagName('a')[0].innerText;

        $.ajax({
            type: 'GET',
            url: '/tabledel?tabname='+tabname,
        });
        tabdiv.parentNode.removeChild(tabdiv);
    }
}
