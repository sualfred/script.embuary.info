#!/usr/bin/python
# coding: utf - 8

movie_certs = {
    'US': [{
            'certification': 'G',
            'order': 1
        },
        {
            'certification': 'PG-13',
            'order': 3
        },
        {
            'certification': 'R',
            'order': 4
        },
        {
            'certification': 'NC-17',
            'order': 5
        },
        {
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'PG',
            'order': 2
        }
    ],
    'CA': [{
            'certification': '18A',
            'order': 4
        },
        {
            'certification': 'G',
            'order': 1
        },
        {
            'certification': 'PG',
            'order': 2
        },
        {
            'certification': '14A',
            'order': 3
        },
        {
            'certification': 'A',
            'order': 5
        }
    ],
    'AU': [{
            'certification': 'E',
            'order': 1
        },
        {
            'certification': 'G',
            'order': 2
        },
        {
            'certification': 'R18+',
            'order': 6
        },
        {
            'certification': 'RC',
            'order': 8
        },
        {
            'certification': 'PG',
            'order': 3
        },
        {
            'certification': 'M',
            'order': 4
        },
        {
            'certification': 'MA15+',
            'order': 5
        },
        {
            'certification': 'X18+',
            'order': 7
        }
    ],
    'DE': [{
            'certification': '0',
            'order': 1
        },
        {
            'certification': '6',
            'order': 2
        },
        {
            'certification': '12',
            'order': 3
        },
        {
            'certification': '16',
            'order': 4
        },
        {
            'certification': '18',
            'order': 5
        }
    ],
    'FR': [{
            'certification': 'U',
            'order': 1
        },
        {
            'certification': '12',
            'order': 3
        },
        {
            'certification': '10',
            'order': 2
        },
        {
            'certification': '16',
            'order': 4
        },
        {
            'certification': '18',
            'order': 5
        }
    ],
    'NZ': [{
            'certification': 'M',
            'order': 3
        },
        {
            'certification': '13',
            'order': 4
        },
        {
            'certification': '15',
            'order': 5
        },
        {
            'certification': 'G',
            'order': 1
        },
        {
            'certification': 'PG',
            'order': 2
        },
        {
            'certification': '16',
            'order': 6
        },
        {
            'certification': '18',
            'order': 7
        },
        {
            'certification': 'R',
            'order': 8
        }
    ],
    'IN': [{
            'certification': 'U',
            'order': 0
        },
        {
            'certification': 'UA',
            'order': 1
        },
        {
            'certification': 'A',
            'order': 2
        }
    ],
    'GB': [{
            'certification': '15',
            'order': 5
        },
        {
            'certification': 'R18',
            'order': 7
        },
        {
            'certification': 'U',
            'order': 1
        },
        {
            'certification': 'PG',
            'order': 2
        },
        {
            'certification': '12A',
            'order': 3
        },
        {
            'certification': '12',
            'order': 4
        },
        {
            'certification': '18',
            'order': 6
        }
    ],
    'NL': [{
            'certification': 'AL',
            'order': 1
        },
        {
            'certification': '6',
            'order': 2
        },
        {
            'certification': '9',
            'order': 3
        },
        {
            'certification': '12',
            'order': 4
        },
        {
            'certification': '16',
            'order': 5
        }
    ],
    'BR': [{
            'certification': 'L',
            'order': 1
        },
        {
            'certification': '10',
            'order': 2
        },
        {
            'certification': '12',
            'order': 3
        },
        {
            'certification': '14',
            'order': 4
        },
        {
            'certification': '16',
            'order': 5
        },
        {
            'certification': '18',
            'order': 6
        }
    ],
    'FI': [{
            'certification': 'S',
            'order': 1
        },
        {
            'certification': 'K-7',
            'order': 2
        },
        {
            'certification': 'K-12',
            'order': 3
        },
        {
            'certification': 'K-16',
            'order': 4
        },
        {
            'certification': 'K-18',
            'order': 5
        },
        {
            'certification': 'KK',
            'order': 6
        }
    ],
    'BG': [{
            'certification': 'A',
            'order': 1
        },
        {
            'certification': 'B',
            'order': 2
        },
        {
            'certification': 'C',
            'order': 3
        },
        {
            'certification': 'D',
            'order': 4
        },
        {
            'certification': 'X',
            'order': 5
        }
    ],
    'ES': [{
            'certification': 'APTA',
            'order': 1
        },
        {
            'certification': '7',
            'order': 2
        },
        {
            'certification': '12',
            'order': 3
        },
        {
            'certification': '16',
            'order': 4
        },
        {
            'certification': '18',
            'order': 5
        },
        {
            'certification': 'X',
            'order': 6
        }
    ],
    'PT': [{
            'certification': 'Públicos',
            'order': 1
        },
        {
            'certification': 'M/3',
            'order': 2
        },
        {
            'certification': 'M/6',
            'order': 3
        },
        {
            'certification': 'M/12',
            'order': 4
        },
        {
            'certification': 'M/14',
            'order': 5
        },
        {
            'certification': 'M/16',
            'order': 6
        },
        {
            'certification': 'M/18',
            'order': 7
        },
        {
            'certification': 'P',
            'order': 8
        }
    ],
    'MY': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'U',
            'order': 1
        },
        {
            'certification': 'P13',
            'order': 2
        },
        {
            'certification': '18SG',
            'order': 3
        },
        {
            'certification': '18SX',
            'order': 4
        },
        {
            'certification': '18PA',
            'order': 5
        },
        {
            'certification': '18PL',
            'order': 6
        }
    ],
    'CA-QC': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'G',
            'order': 1
        },
        {
            'certification': '13+',
            'order': 2
        },
        {
            'certification': '16+',
            'order': 3
        },
        {
            'certification': '18+',
            'order': 4
        }
    ],
    'SE': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'Btl',
            'order': 1
        },
        {
            'certification': '7',
            'order': 2
        },
        {
            'certification': '11',
            'order': 3
        },
        {
            'certification': '15',
            'order': 4
        }
    ],
    'DK': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'A',
            'order': 1
        },
        {
            'certification': '7',
            'order': 2
        },
        {
            'certification': '11',
            'order': 3
        },
        {
            'certification': '15',
            'order': 4
        },
        {
            'certification': 'F',
            'order': 5
        }
    ],
    'NO': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'A',
            'order': 1
        },
        {
            'certification': '6',
            'order': 2
        },
        {
            'certification': '9',
            'order': 3
        },
        {
            'certification': '12',
            'order': 4
        },
        {
            'certification': '15',
            'order': 5
        },
        {
            'certification': '18',
            'order': 6
        }
    ],
    'HU': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'KN',
            'order': 1
        },
        {
            'certification': '6',
            'order': 2
        },
        {
            'certification': '12',
            'order': 3
        },
        {
            'certification': '16',
            'order': 4
        },
        {
            'certification': '18',
            'order': 5
        },
        {
            'certification': 'X',
            'order': 6
        }
    ],
    'LT': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'V',
            'order': 1
        },
        {
            'certification': 'N-7',
            'order': 2
        },
        {
            'certification': 'N-13',
            'order': 3
        },
        {
            'certification': 'N-16',
            'order': 4
        },
        {
            'certification': 'N-18',
            'order': 5
        }
    ],
    'RU': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': '0+',
            'order': 1
        },
        {
            'certification': '6+',
            'order': 2
        },
        {
            'certification': '12+',
            'order': 3
        },
        {
            'certification': '16+',
            'order': 4
        },
        {
            'certification': '18+',
            'order': 5
        }
    ],
    'PH': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'G',
            'order': 1
        },
        {
            'certification': 'PG',
            'order': 2
        },
        {
            'certification': 'R-13',
            'order': 3
        },
        {
            'certification': 'R-16',
            'order': 4
        },
        {
            'certification': 'R-18',
            'order': 5
        },
        {
            'certification': 'X',
            'order': 6
        }
    ],
    'IT': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'T',
            'order': 1
        },
        {
            'certification': 'VM14',
            'order': 2
        },
        {
            'certification': 'VM18',
            'order': 3
        }
    ]
}

tv_certs = {
    'RU': [{
            'certification': '18+',
            'order': 5
        },
        {
            'certification': '0+',
            'order': 1
        },
        {
            'certification': '6+',
            'order': 2
        },
        {
            'certification': '12+',
            'order': 3
        },
        {
            'certification': '16+',
            'order': 4
        }
    ],
    'US': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'TV-Y',
            'order': 1
        },
        {
            'certification': 'TV-Y7',
            'order': 2
        },
        {
            'certification': 'TV-G',
            'order': 3
        },
        {
            'certification': 'TV-PG',
            'order': 4
        },
        {
            'certification': 'TV-14',
            'order': 5
        },
        {
            'certification': 'TV-MA',
            'order': 6
        }
    ],
    'CA': [{
            'certification': 'Exempt',
            'order': 0
        },
        {
            'certification': 'C',
            'order': 1
        },
        {
            'certification': 'C8',
            'order': 2
        },
        {
            'certification': 'G',
            'order': 3
        },
        {
            'certification': 'PG',
            'order': 4
        },
        {
            'certification': '14+',
            'order': 5
        },
        {
            'certification': '18+',
            'order': 6
        }
    ],
    'AU': [{
            'certification': 'P',
            'order': 1
        },
        {
            'certification': 'C',
            'order': 2
        },
        {
            'certification': 'G',
            'order': 3
        },
        {
            'certification': 'PG',
            'order': 4
        },
        {
            'certification': 'M',
            'order': 5
        },
        {
            'certification': 'MA15+',
            'order': 6
        },
        {
            'certification': 'AV15+',
            'order': 7
        },
        {
            'certification': 'R18+',
            'order': 8
        }
    ],
    'FR': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': '10',
            'order': 1
        },
        {
            'certification': '12',
            'order': 2
        },
        {
            'certification': '16',
            'order': 3
        },
        {
            'certification': '18',
            'order': 4
        }
    ],
    'DE': [{
            'certification': '0',
            'order': 0
        },
        {
            'certification': '6',
            'order': 1
        },
        {
            'certification': '12',
            'order': 2
        },
        {
            'certification': '16',
            'order': 3
        },
        {
            'certification': '18',
            'order': 4
        }
    ],
    'TH': [{
            'certification': 'ส',
            'order': 0
        },
        {
            'certification': 'ท',
            'order': 1
        },
        {
            'certification': 'น 13+',
            'order': 2
        },
        {
            'certification': 'น 15+',
            'order': 3
        },
        {
            'certification': 'น 18+',
            'order': 4
        },
        {
            'certification': 'ฉ 20-',
            'order': 5
        },
        {
            'certification': '-',
            'order': 6
        }
    ],
    'KR': [{
            'certification': 'Exempt',
            'order': 0
        },
        {
            'certification': 'ALL',
            'order': 1
        },
        {
            'certification': '7',
            'order': 2
        },
        {
            'certification': '12',
            'order': 3
        },
        {
            'certification': '15',
            'order': 4
        },
        {
            'certification': '19',
            'order': 5
        }
    ],
    'GB': [{
            'certification': 'U',
            'order': 0
        },
        {
            'certification': 'PG',
            'order': 1
        },
        {
            'certification': '12A',
            'order': 2
        },
        {
            'certification': '12',
            'order': 3
        },
        {
            'certification': '15',
            'order': 4
        },
        {
            'certification': '18',
            'order': 5
        },
        {
            'certification': 'R18',
            'order': 6
        }
    ],
    'BR': [{
            'certification': 'L',
            'order': 0
        },
        {
            'certification': '10',
            'order': 1
        },
        {
            'certification': '12',
            'order': 2
        },
        {
            'certification': '14',
            'order': 3
        },
        {
            'certification': '16',
            'order': 4
        },
        {
            'certification': '18',
            'order': 5
        }
    ],
    'NL': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'AL',
            'order': 1
        },
        {
            'certification': '6',
            'order': 2
        },
        {
            'certification': '9',
            'order': 3
        },
        {
            'certification': '12',
            'order': 4
        },
        {
            'certification': '16',
            'order': 5
        }
    ],
    'PT': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'T',
            'order': 1
        },
        {
            'certification': '10AP',
            'order': 2
        },
        {
            'certification': '12AP',
            'order': 3
        },
        {
            'certification': '16',
            'order': 4
        },
        {
            'certification': '18',
            'order': 5
        }
    ],
    'CA-QC': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'G',
            'order': 1
        },
        {
            'certification': '8+',
            'order': 2
        },
        {
            'certification': '13+',
            'order': 3
        },
        {
            'certification': '16+',
            'order': 4
        },
        {
            'certification': '18+',
            'order': 5
        }
    ],
    'HU': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'Unrated',
            'order': 1
        },
        {
            'certification': 'Children',
            'order': 2
        },
        {
            'certification': '6',
            'order': 3
        },
        {
            'certification': '12',
            'order': 4
        },
        {
            'certification': '16',
            'order': 5
        },
        {
            'certification': '18',
            'order': 6
        }
    ],
    'LT': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'N-7',
            'order': 1
        },
        {
            'certification': 'N-14',
            'order': 2
        },
        {
            'certification': 'S',
            'order': 3
        }
    ],
    'PH': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'G',
            'order': 1
        },
        {
            'certification': 'PG',
            'order': 2
        },
        {
            'certification': 'SPG',
            'order': 3
        },
        {
            'certification': 'X',
            'order': 4
        }
    ],
    'ES': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': 'Infantil',
            'order': 1
        },
        {
            'certification': 'TP',
            'order': 2
        },
        {
            'certification': '7',
            'order': 3
        },
        {
            'certification': '10',
            'order': 4
        },
        {
            'certification': '12',
            'order': 5
        },
        {
            'certification': '13',
            'order': 6
        },
        {
            'certification': '16',
            'order': 7
        },
        {
            'certification': '18',
            'order': 8
        }
    ],
    'SK': [{
            'certification': 'NR',
            'order': 0
        },
        {
            'certification': '7',
            'order': 1
        },
        {
            'certification': '12',
            'order': 2
        },
        {
            'certification': '15',
            'order': 3
        },
        {
            'certification': '18',
            'order': 4
        }
    ]
}