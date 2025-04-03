import smartsheet
from django.http import JsonResponse
from django.shortcuts import render  # <-- Make sure you import render if you use render()

def fetch_workspaces(request):
    access_token = "4rJ6r2YBZ5ZUbHgw4QVGuybX6rBEiQ8c16O2S"

    try:
        client = smartsheet.Smartsheet(access_token)
        response = client.Workspaces.list_workspaces(include_all=True)

        data = []
        for ws in response.data:
            data.append({
                "id": ws.id,
                "name": ws.name,
                "accessLevel": str(ws.access_level) if ws.access_level else None
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def workspace_detail(request, workspace_id):
    client = smartsheet.Smartsheet("YOUR_SMARTSHEET_TOKEN")

    try:
        workspace_info = client.Workspaces.get_workspace(workspace_id)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    data = {
        "id": workspace_info.id,
        "name": workspace_info.name,
        "sheets": []
    }

    for sheet in workspace_info.sheets:
        data["sheets"].append({
            "sheetId": sheet.id,
            "sheetName": sheet.name
        })

    # We'll use an HTML template called workspace_detail.html
    return render(request, "workspace_detail.html", {"workspace": data})
