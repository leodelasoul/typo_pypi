rule pypi
{
    strings:
        $re3 = "UNKNOWN"
    condition:
        #re3 > 2
}