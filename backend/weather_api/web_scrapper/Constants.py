PARAMETERS = ["Tmax","Tmin","Tmean","Sunshine","Rainfall","Raindays1mm","AirFrost"]
REGIONS = ["UK","England","Wales","Scotland","Northern_Ireland","England_and_Wales","England_N","England_S",
                        "Scotland_N","Scotland_E","Scotland_W","England_E_and_NE","England_NW_and_N_Wales","Midlands","East_Angelia",
                        "England_SW_and_S_Wales","England_SE_and_Central_S"]
new_columns= {"win":"winter","spr":"spring","aut":"autmn","sum":"summer","ann":"annual",
            "jan":"january","feb":"february","mar":"march","apr":"april","may":"may",
            "jun":"june","jul":"july","aug":"august","sep":"september","oct":"october",
            "nov":"november","dec":"december"}

month_columns = ["year","january","february","march","april","may",
            "june","july","august","september","october",
            "november","december"]

season_columns = ["winter","spring","autmn","summer","year"]