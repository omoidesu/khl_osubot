color = {0 : "#EA669E" , 1 :"#E44116" , 2:"#71368A" , 3:"#66CCFF"}

def cardHead(mode):
    card_head = f'''[
    {{
        "type": "card",
        "theme": "secondary",
        "color": "{color[mode]}",
        "size": "lg",
        "modules": ['''
    
    return card_head

def cardScore(score , maxcombo , pp , mode):
    if mode < 2:
        if mode == 0:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n[**{score.c300}** / {score.c100} / {score.c50} / {score.cmiss}]"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo}x / **{maxcombo}x**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "{pp} **pp**\\n**Score** {score.score}"
                        }}
                    ]
                }}
            }}'''
        else:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n[**{score.c300 + score.cgeki}** / {score.c100 + score.ckatu} / {score.cmiss}]"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo}x / **{maxcombo}x**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "{pp} **pp**\\n**Score** {score.score}"
                        }}
                    ]
                }}
            }}'''
    else:
        if mode == 2:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n[**{score.c300}** / {score.c100} / {score.ckatu} / {score.cmiss}]"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo}x / {maxcombo}x"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "{pp} **pp**\\n**Score** {score.score}"
                        }}
                    ]
                }}
            }}'''
        else:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n{pp} **pp**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo} **combo**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**Score** {score.score}"
                        }}
                    ]
                }}
                }},{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "**max** : {score.cgeki}\\n**300** : {score.c300}"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**200** : {score.ckatu}\\n**100** : {score.c100}"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**  50  **: {score.c50}\\n**miss** : {score.cmiss}"
                        }}
                    ]
                }}
            }}'''
    
    return game_result

def cardBp(score ,bmap ,bmapset ,bp , num , maxcombo , bstatus , ranking , mod , mode , coverurl):
    if mode == 3:
        result = f'''{{
              "type": "kmarkdown",
              "content": "      **BP{num}**\\n\\n    **{score.score}**"
            }},
            {{
              "type": "kmarkdown",
              "content": "**{score.acc}%**\\n{score.combo}x\\n{bmap.stars}★"
            }},
            {{
              "type": "kmarkdown",
              "content": "**{score.pp} PP**\\nweight: {bp.percent}%\\n{bp.pp_after} pp"
            }}'''
    else:
        result = f'''{{
                        "type": "kmarkdown",
                        "content": "\\n     **BP{num}**\\n"
                    }},
                    {{
                        "type": "kmarkdown",
                        "content": "**{score.acc}%**\\n{score.combo}x / **{maxcombo}x**\\n{bmap.stars}★"
                    }},
                    {{
                        "type": "kmarkdown",
                        "content": "**{score.pp} PP**\\nweight: {bp.percent}%\\n{bp.pp_after} pp"
                    }}'''

    bpmsg = f'''{{
            "type": "section",
            "text": {{
                "type": "paragraph",
                "cols": 3,
                "fields": [{result}
                ]
            }},
            "mode": "right",
            "accessory": {{
                "type": "image",
                "src": "{coverurl}",
                "size": "sm"
            }}
        }},
        {{
            "type": "context",
            "elements": [
                {{
                    "type": "image",
                    "src": "{bstatus[score.mode]}"
                }},
                {{
                    "type": "plain-text",
                    "content": " | "
                }},
                {{
                    "type": "image",
                    "src": "{ranking[score.rank]}"
                }},
                {{
                    "type": "plain-text",
                    "content": " | mods: "
                }},
                {mod}
                {{
                    "type": "plain-text",
                    "content": " | {score.playTime}\\n"
                }}
            ]
        }},
        {{
            "type": "section",
            "text" : {{
            "type": "kmarkdown",
            "content": "下载地址：[ppy](https://osu.ppy.sh/beatmapsets/{bmap.setid}#osu/{bmap.mapid}) | [sayo](https://txy1.sayobot.cn/beatmaps/download/novideo/{bmap.mapid}) | [chimu](https://api.chimu.moe/v1/download/{bmap.mapid}?n=1) | [btct](https://beatconnect.io/b/{bmap.mapid}) | [nerina](https://nerina.pw/d/{bmap.mapid})"
            }}
        }},
        {{
            "type": "audio",
            "title": "{bmapset.title}",
            "src": "{bmapset.mp3}",
            "cover": "{coverurl}"
        }}
        ,{{"type": "divider"}}'''

    return bpmsg
