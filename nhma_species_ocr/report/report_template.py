
def report_template(entries: list[str] = []):
    entries_html = ''.join(entries)
    return """

<html>
<meta charset="UTF-8">

<style>
    .equal {
        box-shadow: inset 0 -0.5vw 0 0 rgb(178, 250, 173);
    }

    .different {
        box-shadow: inset 0 -0.5vw 0 0 rgb(251, 255, 126);
    }

    .error {
        box-shadow: inset 0 -0.5vw 0 0 rgb(255, 150, 147);
    }

    body {
        background-color: rgb(241, 241, 241);
    }

    .card {
        background-color: rgb(255, 255, 255);
        box-shadow: .3vw .3vw 1vw rgb(197, 197, 197);
        display: flex;
        border-radius: .3vw;
        padding: 1vw;
        min-height: 33vw;
    }

    .card-container {
        font-size: 1.5vw;
        margin: 8vw;
    }

    .card-top {
        margin-inline: 1vw;
        display: flex;
        justify-content: space-between;
    }

    h4 {
        margin-bottom: 1vw;
    }

    .left {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 42%;
    }

    .ocr {
        text-align: left;
        margin-top: 1vw;
        height: 100%;
        max-height: 50%;
        padding-inline: 1vw;
        padding-block: .6vw;
        border: .1vw solid black;
    }

    .ocr div {
        padding-block: .4vw;
    }

    .right {
        margin-left: 1vw;
        width: 58%;
        height: 100%;
    }

    img {
        max-width: 100%;
        max-height: 100%;
        border: .1vw solid black;
    }

    table {
        height: 80%;
        width: 100%;
    }

    .center {
        margin-left: .5vw;
        display: flex;
        justify-content: left;
        width: 100%;
        text-align: center;
        align-items: center;
    }

    td {
        padding-left: 1vw;
    }

    th {
        text-align: right;
        font-family: Arial, Helvetica, sans-serif;
        font-size: .8vw;
        font-style: oblique;
    }

    .title {
        padding-top: 4vw;
        padding-bottom: 1.5vw;
        text-align: center;
        width: 46%;
    }

    .card,
    td {
        font-size: 1.3vw;
        font-family: 'Courier New', Courier, monospace;
    }

    td,
    th {
        height: 4.8vw;
    }

    table,
    tr {
        border-collapse: collapse;
        border-bottom: .1vw solid black;
    }

    .top-row {
        padding-bottom: 2.5vw;
    }
</style>

<body>
""" + entries_html + """
</body>

</html>

"""