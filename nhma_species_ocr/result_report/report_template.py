
report_template = """
<html>
    <meta charset="UTF-8">
    <body>
        <table>
            <tr>
                <th>
                    Label
                </th>
                <th>
                    Område læst
                </th>
                <th>
                    Område opslag
                </th>
                <th>
                    Navn læst
                </th>
                <th>
                    Navn opslag
                </th>
            </tr>
            {0}
        </table>
    </body>
</html>

<style>
    table, th, td {
        border: 1px solid;
    }
    th, td {
        padding: 10px;
    }
</style>
"""