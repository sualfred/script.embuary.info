# script.embuary.info

Script to provide skinners the option to call The Movie DB for actor and video infos.
Unlike ExtendedInfo it requires a skin integration and it does not include a browser and it only crawls for the most basic and required information.

## Search by string

Examles
*  ```RunScript(script.embuary.info,call=person,query='"Bruce Willis"'```
*  ```RunScript(script.embuary.info,call=tv,query='"Californication"'```
*  ```RunScript(script.embuary.info,call=movie,query='"Iron Man"'```

`'" "'` is not required, but useful if a string contains special characters. which needs to be escaped.

*Multiple results*
The script provides a selection dialog if multiple results were returned.

## Search by The Movie DB ID

If the real TMDB ID is available it's possible to call the information directly.
*  ```RunScript(script.embuary.info,call=person,tmbd_id=65```
*  ```RunScript(script.embuary.info,call=tv,tmbd_id=65```
*  ```RunScript(script.embuary.info,call=movie,tmbd_id=65```

## Options

* An API key is already shipped but can be replaced in the add-on settings
* EN is used as default language. It can be changed in the add-on settings, but will still be used if important informations are missing from the result (The Movie DB doesn't have a own fallback logic).

## Required windows and reserved IDs
*Important*
* I hate it if a script takes control about the focus. Because of that it's up to the skinner to add a `<defaultcontrol>` tag.
* `ListItem.DBID` is filled if the found item is part of the local library.
* All actions on the control IDs below are controlled by the script. 
* The script doesn't set any window property for the called item. You have to call it from the main container. Examples: `$INFO[Container(10051).ListItem.Directors]`, `$INFO[Container(10051).ListItem.Rating]`, `$INFO[Container(10051).ListItem.Art(thumb)]`

*script-embuary-person.xml*
* List control ID `10051` = All available information of the called person.
* List control ID `10052` = All movies starring with actor xyz
* List control ID `10053` = All shows starring with actor xyz
* List control ID `10054` = Actor portraits

*script-embuary-video.xml*
* List control ID `10051` = All available information of the called item.
* List control ID `10052` = Cast
* List control ID `10053` = Similar titles
* List control ID `10054` = YouTube results
* List control ID `10055` = Backdrop images

*script-embuary-image.xml*
* Image control ID `1` = Is used to display a portrait/backdrop image in fullscreen. 


