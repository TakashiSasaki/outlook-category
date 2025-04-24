# Export-OutlookCategoriesToJson.ps1
# Collects all Outlook category data across accounts and exports it as JSON.

# Create Outlook COM object
$outlook = New-Object -ComObject Outlook.Application

# Get MAPI namespace
$namespace = $outlook.GetNamespace("MAPI")

# Prepare list to hold all category info
$allCategories = @()

# Enumerate all Outlook stores (accounts)
foreach ($store in $namespace.Stores) {
    $storeName = $store.DisplayName
    $session = $store.GetRootFolder().Session
    $categories = $session.Categories

    foreach ($category in $categories) {
        $categoryInfo = [ordered]@{}
        $categoryInfo["Account"] = $storeName

        # Add all properties dynamically
        $properties = $category | Get-Member -MemberType Property
        foreach ($prop in $properties) {
            $propName = $prop.Name
            $propValue = $category.$propName
            $categoryInfo[$propName] = $propValue
        }

        $allCategories += [PSCustomObject]$categoryInfo
    }
}

# Convert to JSON (with depth for nested structures if needed)
$allCategories | ConvertTo-Json -Depth 5
