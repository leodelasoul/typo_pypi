rule pypi
{
    strings:
        $re1 = "UNKNOWN"
        $re2 = /"description": ""/
        $re3 = /"description": "UNKNOWN"/

    condition:
        #re1 > 2 or ($re2 or $re3)
}
