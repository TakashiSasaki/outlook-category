<#
.SYNOPSIS
Exports all Outlook categories across all MAPI stores into a JSON file.

.DESCRIPTION
Uses the Outlook COM API to enumerate categories in each store, and outputs either
a simplified or detailed JSON representation. If -Detailed is specified, includes
full summaries of Application and Session COM objects; otherwise outputs only
essential fields.

.PARAMETER OutputPath
Path to the JSON file to write. If omitted, defaults to "categories-YYYYMMDD.json".

.PARAMETER Detailed
Switch. When present, outputs full property details (Application, Session, Parent, etc).
#>

param (
    [string]$OutputPath,
    [switch]$Detailed
)

# Default output filename: categories-YYYYMMDD.json
if (-not $OutputPath) {
    $OutputPath = "categories-$(Get-Date -Format 'yyyyMMdd').json"
}

# Map of OlObjectClass codes to names
$OlObjectClassMap = @{
    152 = 'olCategory'
    153 = 'olCategories'
}

function Resolve-OlObjectClassName {
    param([int]$Value)
    if ($OlObjectClassMap.ContainsKey($Value)) {
        return $OlObjectClassMap[$Value]
    } else {
        return "Unknown($Value)"
    }
}

# Create Outlook COM application and namespace
$outlook   = New-Object -ComObject Outlook.Application
$namespace = $outlook.GetNamespace('MAPI')

$allCategories = @()

foreach ($store in $namespace.Stores) {
    $storeName  = $store.DisplayName
    $session    = $store.GetRootFolder().Session
    $categories = $session.Categories

    foreach ($category in $categories) {
        $info = New-Object System.Collections.Specialized.OrderedDictionary

        # Common fields
        $info["Account"]    = $storeName
        $info["CategoryID"] = $category.CategoryID
        $info["Color"]      = $category.Color
        $info["Name"]       = $category.Name

        $classVal = $category.Class
        $info["ClassName"] = Resolve-OlObjectClassName -Value $classVal

        if ($Detailed) {
            # Full Application summary
            $appSummary = New-Object System.Collections.Specialized.OrderedDictionary
            $appSummary["TypeName"] = $outlook.GetType().FullName
            $appSummary["ToString"] = $outlook.ToString()
            $appSummary["Version"]  = $outlook.Version
            try { $appSummary["Name"] = $outlook.Name } catch { $appSummary["Name"] = "N/A" }
            $info["Application"] = $appSummary

            # Full Session summary
            $sessionSummary = New-Object System.Collections.Specialized.OrderedDictionary
            $sessionSummary["TypeName"]  = $session.GetType().FullName
            $sessionSummary["ToString"]  = $session.ToString()
            try { $sessionSummary["CurrentUser"] = $session.CurrentUser.Name } catch { $sessionSummary["CurrentUser"] = "N/A" }
            try { $sessionSummary["DefaultStore"] = $session.DefaultStore.DisplayName } catch { $sessionSummary["DefaultStore"] = "N/A" }
            $sessionSummary["StoresCount"] = $namespace.Stores.Count
            $info["Session"] = $sessionSummary

            # Parent summary
            try {
                $parent = $category.Parent
                $parentSummary = New-Object System.Collections.Specialized.OrderedDictionary
                $parentSummary["TypeName"]  = $parent.GetType().FullName
                $parentSummary["ToString"]  = $parent.ToString()
                try { $parentSummary["Count"] = $parent.Count } catch { $parentSummary["Count"] = "N/A" }

                try {
                    $pc = $parent.GetType().InvokeMember("Class", [Reflection.BindingFlags]::GetProperty, $null, $parent, $null)
                    $parentSummary["PossibleClass"] = $pc
                    $parentSummary["ParentPossibleClassName"] = Resolve-OlObjectClassName -Value $pc
                } catch {
                    $parentSummary["PossibleClass"] = "Unknown"
                    $parentSummary["ParentPossibleClassName"] = "Unknown"
                }

                $info["Parent"] = $parentSummary
            } catch {
                $info["Parent"] = "Unavailable"
            }

            # Include any other properties
            $excluded = @("Application","Session","Parent","CategoryID","Color","Name","Class")
            $props = $category | Get-Member -MemberType Property
            foreach ($p in $props) {
                if ($excluded -contains $p.Name) { continue }
                try { $info[$p.Name] = $category.$($p.Name) } catch {}
            }
        }
        else {
            # Simplified Application/Session info
            $info["Application.Name"]    = $outlook.Name
            $info["Application.Version"] = $outlook.Version
            try { $info["Session.CurrentUser"]  = $session.CurrentUser.Name } catch { $info["Session.CurrentUser"]  = "N/A" }
            try { $info["Session.DefaultStore"] = $session.DefaultStore.DisplayName } catch { $info["Session.DefaultStore"] = "N/A" }
        }

        $allCategories += [PSCustomObject]$info
    }
}

# Convert to JSON
$json = $allCategories | ConvertTo-Json -Depth 6

# Save to file
$json | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Export complete: $OutputPath"
