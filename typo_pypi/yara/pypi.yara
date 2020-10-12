rule pypi
{
    strings:
        $re1 = "UNKNOWN"
        $re2 = /"description": ""/

    condition:
        #re1 > 3 and #re2 > 1
}