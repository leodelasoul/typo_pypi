rule Win32_Trojan_Emotet : tc_detection malicious
{
    meta:

        author              = "ReversingLabs"

        source              = "ReversingLabs"
        status              = "RELEASED"
        sharing             = "TLP:WHITE"
        category            = "MALWARE"
        malware             = "EMOTET"
        description         = "Yara rule that detects Emotet trojan."

        tc_detection_type   = "Trojan"
        tc_detection_name   = "Emotet"
        tc_detection_factor = 5

    strings:

        $decrypt_resource_v1 = {
            55 8B EC 83 EC ?? 53 8B D9 8B C2 56 57 89 45 ?? 8B 3B 33 F8 8B C7 89 7D ?? 83 E0 ?? 
            75 ?? 8D 77 ?? EB ?? 8B F7 2B F0 83 C6 ?? 8D 0C 36 E8 ?? ?? ?? ?? 8B D0 89 55 ?? 85 
            D2 74 ?? 83 65 ?? ?? 8D 43 ?? 83 65 ?? ?? C1 EE ?? 8D 0C B0 8B F2 8B D9 2B D8 83 C3 
            ?? C1 EB ?? 3B C1 0F 47 5D ?? 85 DB 74 ?? 8B 55 ?? 8B F8 8B 0F 8D 7F ?? 33 CA 0F B6 
            C1 66 89 06 8B C1 C1 E8 ?? 8D 76 ?? 0F B6 C0 66 89 46 ?? C1 E9 ?? 0F B6 C1 66 89 46 
            ?? C1 E9 ?? 0F B6 C1 66 89 46 ?? 8B 45 ?? 40 89 45 ?? 3B C3 72 ?? 8B 7D ?? 8B 55 ?? 
            33 C0 66 89 04 7A 5F 5E 8B C2 5B 8B E5 5D C3 
        }

        $generate_filename_v1 = {
            56 57 33 C0 BF ?? ?? ?? ?? 57 50 50 6A ?? 50 FF 15 ?? ?? ?? ?? BA ?? ?? ?? ?? B9 ?? 
            ?? ?? ?? E8 ?? ?? ?? ?? 68 ?? ?? ?? ?? 57 8B F0 56 68 ?? ?? ?? ?? 57 FF 15 ?? ?? ?? 
            ?? 83 C4 ?? 8B CE 5F 5E E9
        }

        $decrypt_resource_v2 = {
            55 8B EC 83 EC ?? 8B 41 ?? 8B 11 33 C2 53 56 8D 71 ?? 89 55 ?? 8D 58 ?? 89 45 ?? 83 
            C6 ?? F6 C3 ?? 74 ?? 83 E3 ?? 83 C3 ?? B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 
            8B C8 E8 ?? ?? ?? ?? FF D0 8D 14 1B B9 ?? ?? ?? ?? 52 6A ?? 50 E8 ?? ?? ?? ?? BA ?? 
            ?? ?? ?? 8B C8 E8 ?? ?? ?? ?? FF D0 89 45 ?? 85 C0 74 ?? C1 EB ?? 8B C8 57 33 C0 8D 
            14 9E 33 DB 8B FA 2B FE 83 C7 ?? C1 EF ?? 3B F2 0F 47 F8 85 FF 74 ?? 8B 16 8D 49 ?? 
            33 55 ?? 8D 76 ?? 0F B6 C2 43 66 89 41 ?? 8B C2 C1 E8 ?? 0F B6 C0 66 89 41 ?? C1 EA 
            ?? 0F B6 C2 66 89 41 ?? C1 EA ?? 0F B6 C2 66 89 41 ?? 3B DF 72 ?? 8B 45 ?? 33 D2 8B 
            4D ?? 5F 66 89 14 41 8B C1 5E 5B 8B E5 5D C3 
        }

        $generate_filename_v2 = {
            55 8B EC 81 EC ?? ?? ?? ?? 8D 85 ?? ?? ?? ?? 50 6A ?? 6A ?? 51 6A ?? B9 ?? ?? ?? ?? 
            E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 8B C8 E8 ?? ?? ?? ?? FF D0 85 C0 0F 88 ?? ?? ?? ?? 56 
            B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? 8B 15 ?? ?? ?? ?? 8B F0 8D 85 ?? ?? ?? ?? 8D [1-5] 51 
            51 50 56 8D [1-5] 68 ?? ?? ?? ?? 51 B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 8B 
            C8 E8 ?? ?? ?? ?? FF D0 83 C4 ?? B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 8B C8 
            E8 ?? ?? ?? ?? FF D0 56 6A ?? 50 B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 8B C8 
            E8 ?? ?? ?? ?? FF D0 B8 ?? ?? ?? ?? 5E 8B E5 5D C3 33 C0 8B E5 5D C3 
        }

        $decrypt_resource_v3 = {
            56 8B F1 BA [6-9] B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? 59 FF D0 56 6A ?? 50 68 ?? ?? ?? ?? 
            BA ?? ?? ?? ?? B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? 59 FF D0 5E C3 
        }

        $generate_filename_v3 = {
            55 8B EC 81 EC ?? ?? ?? ?? 53 56 57 8B F1 8B FA 6A ?? 8D 4D ?? E8 ?? ?? ?? ?? BB ?? 
            ?? ?? ?? 8D 8D ?? ?? ?? ?? 53 E8 ?? ?? ?? ?? 53 8D 8D ?? ?? ?? ?? E8 ?? ?? ?? ?? 83 
            C4 ?? 8D 85 ?? ?? ?? ?? BB ?? ?? ?? ?? 8B D3 56 50 BE ?? ?? ?? ?? [2-5] 8B CE E8 ?? 
            ?? ?? ?? 59 FF D0 57 8D 85 ?? ?? ?? ?? 8B D3 50 [2-5] 8B CE E8 ?? ?? ?? ?? 59 FF D0 
            8D 85 ?? ?? ?? ?? C7 45 ?? ?? ?? ?? ?? 89 45 ?? BA ?? ?? ?? ?? 8D 85 ?? ?? ?? ?? B9 
            ?? ?? ?? ?? 89 45 ?? B8 ?? ?? ?? ?? 66 89 45 ?? 8D 45 ?? 50 68 ?? ?? ?? ?? E8 ?? ?? 
            ?? ?? 59 FF D0 F7 D8 5F 1B C0 5E 40 5B 8B E5 5D C3 
        }

        $decrypt_resource_v4 = {
            56 57 8B FA E8 ?? ?? ?? ?? 8B F0 A1 ?? ?? ?? ?? 85 C0 75 ?? B9 ?? ?? ?? ?? E8 ?? ?? 
            ?? ?? BA ?? ?? ?? ?? 8B C8 E8 ?? ?? ?? ?? A3 ?? ?? ?? ?? 56 FF D0 8B 0D ?? ?? ?? ?? 
            89 44 B9 ?? A1 ?? ?? ?? ?? 85 C0 75 ?? B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 
            8B C8 E8 ?? ?? ?? ?? A3 ?? ?? ?? ?? FF D0 8B F8 A1 ?? ?? ?? ?? 85 C0 75 ?? B9 ?? ?? 
            ?? ?? E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 8B C8 E8 ?? ?? ?? ?? A3 ?? ?? ?? ?? 56 6A ?? 57 
            FF D0 5F 5E C3 
        }

        $generate_filename_snippet_v4 = {
            A1 ?? ?? ?? ?? 85 C0 75 ?? B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? BA ?? ?? ?? ?? 8B C8 E8 ?? 
            ?? ?? ?? A3 ?? ?? ?? ?? 56 53 FF D0 A1 ?? ?? ?? ?? 85 C0 75 ?? B9 ?? ?? ?? ?? E8 ?? 
            ?? ?? ?? BA ?? ?? ?? ?? 8B C8 E8 ?? ?? ?? ?? A3 ?? ?? ?? ?? 56 FF D0 5F 5E 33 C9 8D 
            04 43 66 89 08 5D 5B 59 C3 
        }

    condition:
        uint16(0) == 0x5A4D and 
        (
            $decrypt_resource_v1 and 
            $generate_filename_v1
        ) or 
        (
            $decrypt_resource_v2 and 
            $generate_filename_v2
        ) or
        (
            $decrypt_resource_v3 and 
            $generate_filename_v3
        ) or
        (
            $decrypt_resource_v4 and 
            $generate_filename_snippet_v4
        )
}