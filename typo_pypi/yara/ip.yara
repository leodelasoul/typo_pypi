rule IP {

    strings:
        $ip =  /"IP"/
        $flaged_mal = /(from pydomain)/
    condition:
        $ip or $flaged_mal

}