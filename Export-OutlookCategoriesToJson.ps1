# Export-OutlookCategoriesToJson.ps1
# Export Outlook category info with optional detailed output.

param (
    [string]$OutputFile,
    [switch]$Detailed
)

if (-not $OutputFile) {
    $OutputFile = "categories-$(Get-Date -Format 'yyyyMMdd').json"
}

# Mapping for OlObjectClass
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

# COM objects
$outlook   = New-Object -ComObject Outlook.Application
$namespace = $outlook.GetNamespace('MAPI')

$allCategories = @()

foreach ($store in $namespace.Stores) {
    $storeName  = $store.DisplayName
    $session    = $store.GetRootFolder().Session
    $categories = $session.Categories

    foreach ($category in $categories) {
        $info = New-Object System.Collections.Specialized.OrderedDictionary

        # Basic common fields
        $info["Account"]     = $storeName
        $info["CategoryID"]  = $category.CategoryID
        $info["Color"]       = $category.Color
        $info["Name"]        = $category.Name

        $classVal = $category.Class
        $info["ClassName"] = Resolve-OlObjectClassName -Value $classVal

        if ($Detailed) {
            # Full Application object
            $appSummary = New-Object System.Collections.Specialized.OrderedDictionary
            $appSummary["TypeName"] = $outlook.GetType().FullName
            $appSummary["ToString"] = $outlook.ToString()
            $appSummary["Version"]  = $outlook.Version
            try { $appSummary["Name"] = $outlook.Name } catch { $appSummary["Name"] = "N/A" }
            $info["Application"] = $appSummary

            # Full Session object
            $sessionSummary = New-Object System.Collections.Specialized.OrderedDictionary
            $sessionSummary["TypeName"] = $session.GetType().FullName
            $sessionSummary["ToString"] = $session.ToString()
            try { $sessionSummary["CurrentUser"] = $session.CurrentUser.Name } catch { $sessionSummary["CurrentUser"] = "N/A" }
            try { $sessionSummary["DefaultStore"] = $session.DefaultStore.DisplayName } catch { $sessionSummary["DefaultStore"] = "N/A" }
            $sessionSummary["StoresCount"] = $namespace.Stores.Count
            $info["Session"] = $sessionSummary

            # Parent summary
            try {
                $parent = $category.Parent
                $parentSummary = New-Object System.Collections.Specialized.OrderedDictionary
                $parentSummary["TypeName"] = $parent.GetType().FullName
                $parentSummary["ToString"] = $parent.ToString()
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

            # All other properties
            $excluded = @("Application", "Session", "Parent", "CategoryID", "Color", "Name", "Class")
            $props = $category | Get-Member -MemberType Property
            foreach ($p in $props) {
                $pn = $p.Name
                if ($excluded -contains $pn) { continue }
                try { $info[$pn] = $category.$pn } catch {}
            }
        }
        else {
            # Simple application/session info only
            $info["Application.Name"]    = $outlook.Name
            $info["Application.Version"] = $outlook.Version
            try { $info["Session.CurrentUser"]   = $session.CurrentUser.Name } catch { $info["Session.CurrentUser"] = "N/A" }
            try { $info["Session.DefaultStore"]  = $session.DefaultStore.DisplayName } catch { $info["Session.DefaultStore"] = "N/A" }
        }

        $allCategories += [PSCustomObject]$info
    }
}

$allCategories |
    ConvertTo-Json -Depth 6 |
    Out-File -Encoding UTF8 $OutputFile

Write-Host "Export complete: $OutputFile"
