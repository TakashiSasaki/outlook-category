<#
.SYNOPSIS
  Export Outlook categories via COM API into a JSON file keyed by schema UUID.

.DESCRIPTION
  Connects to Outlook via COM and collects all categories from all stores.
  Outputs a JSON object of the form:
    {
      "<schema-uuid>": [ {Category1}, {Category2}, … ]
    }
  Writes to the path given by -OutputPath (defaults to OutlookCategories-<yyyyMMdd>.json).

.PARAMETER OutputPath
  Path to write the JSON output. Defaults to:
    OutlookCategories-<yyyyMMdd>.json

.EXAMPLE
  .\Export-OutlookCategoriesToJson.ps1 -OutputPath OutlookCategories.json
#>

param(
    [Parameter(Mandatory = $false)]
    [string] $OutputPath = ("OutlookCategories-{0:yyyyMMdd}.json" -f (Get-Date))
)

# The schema UUID to use as the property name
$SchemaUuid = '8f87b8d1-cc90-4e92-b295-b2222efcbf28'

# Map of OlObjectClass codes to names
$OlClassMap = @{
    152 = 'olCategory'
    153 = 'olCategories'
}

function Resolve-ClassName {
    param([int] $Value)
    # Use -or to fall back if the map lookup returns $null
    return $OlClassMap[$Value] ?? "Unknown($Value)"
}

# Initialize Outlook COM objects
$Outlook   = New-Object -ComObject Outlook.Application
$Namespace = $Outlook.GetNamespace('MAPI')

# Gather all categories into an array of PSCustomObject
$AllCategories = @()
foreach ($Store in $Namespace.Stores) {
    $StoreName = $Store.DisplayName
    $Session   = $Store.GetRootFolder().Session
    foreach ($Category in $Session.Categories) {
        $AllCategories += [PSCustomObject]@{
            Account               = $StoreName
            CategoryID            = $Category.CategoryID
            Color                 = $Category.Color
            Name                  = $Category.Name
            ClassName             = Resolve-ClassName -Value $Category.Class
            'Application.Name'    = $Outlook.Name
            'Application.Version' = $Outlook.Version
            'Session.CurrentUser' = $Session.CurrentUser.Name
            'Session.DefaultStore'= $Session.DefaultStore.DisplayName
        }
    }
}

# Wrap under the UUID key
$OutputObject = @{ $SchemaUuid = $AllCategories }

# Serialize to compact JSON (PowerShell 7+)
$Json = $OutputObject |
    ConvertTo-Json -Depth 4 -Compress

# Write UTF-8 file
Set-Content -Path $OutputPath -Value $Json -Encoding UTF8

Write-Host "[Export] JSON written to $OutputPath"
