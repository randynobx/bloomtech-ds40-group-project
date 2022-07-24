"""Tests for loaders.ingest_games"""

from bs4 import BeautifulSoup
from loaders.boardgame_db_classes import Game, GameCategoryMap, GameMechanicMap
from loaders import ingest_games

def test_ingest_game():
    test_ret = ingest_games.ingest_game(game_soup)
    assert isinstance(test_ret, Game), 'Did not return Game object'
    assert test_ret.id == 72125, 'Incorrect ID returned'
    assert test_ret.title == 'Eclipse', 'Incorrect Title returned'


def test_ingest_game_mech_mapping():
    test_ret = ingest_games.ingest_game_mech_mapping(game_soup)
    assert isinstance(test_ret, list), 'Did not return list'
    for item in test_ret:
        assert isinstance(item, GameMechanicMap), \
            'Returned a non-GameMechanicMap object'
        assert item.game_id.isdigit(), 'Invalid GameID returned'
        assert item.mechanic_id.isdigit(), 'Invalid MechanicID returned'
        
    # <link type="boardgamemechanic" id="2011" value="Modular Board" />


def test_ingest_game_cat_mapping():
    test_ret = ingest_games.ingest_game_cat_mapping(game_soup)
    assert isinstance(test_ret, list), 'Did not return list'
    for item in test_ret:
        assert isinstance(item, GameCategoryMap), \
            'Returned a non-GameCategoryMap object'
        assert item.game_id.isdigit(), 'Invalid GameID returned'
        assert item.category_id.isdigit(), 'Invalid CategoryID returned'


xml = '''
<item type="boardgame" id="72125">
         <thumbnail>https://cf.geekdo-images.com/cnFppsVNOSTJ-W3APQFuTg__thumb/img/X8XQO2_mRl7HRSzzOEgoKrWulj4=/fit-in/200x150/filters:strip_icc()/pic1974056.jpg</thumbnail>
      <image>https://cf.geekdo-images.com/cnFppsVNOSTJ-W3APQFuTg__original/img/AbcjscBi-x3tVrsJsBhXq2RxLbc=/0x0/filters:format(jpeg)/pic1974056.jpg</image>
                                     				
				<name type="primary" sortindex="1" value="Eclipse" />
			
						                               				
				<name type="alternate" sortindex="1" value="星蚀" />
			    				
				<name type="alternate" sortindex="1" value="이클립스" />
			
						               													<description>The galaxy has been a peaceful place for many years. After the ruthless Terran&amp;ndash;Hegemony War (30.027&amp;ndash;33.364), much effort has been employed by all major spacefaring species to prevent the terrifying events from repeating themselves. The Galactic Council was formed to enforce precious peace, and it has taken many courageous efforts to prevent the escalation of malicious acts. Nevertheless, tension and discord are growing among the seven major species and in the Council itself. Old alliances are shattering, and hasty diplomatic treaties are made in secrecy. A confrontation of the superpowers seems inevitable &amp;ndash; only the outcome of the galactic conflict remains to be seen. Which faction will emerge victorious and lead the galaxy under its rule?&amp;#10;&amp;#10;A game of Eclipse places you in control of a vast interstellar civilization, competing for success with its rivals. You will explore new star systems, research technologies, and build spaceships with which to wage war. There are many potential paths to victory, so you need to plan your strategy according to the strengths and weaknesses of your species, while paying attention to the other civilizations' endeavors.&amp;#10;&amp;#10;The shadows of the great civilizations are about to eclipse the galaxy. Lead your people to victory!&amp;#10;&amp;#10;</description>
										      	               				<yearpublished value="2011" />
						               				<minplayers value="2" />
						               				<maxplayers value="6" />
						      			<poll name="suggested_numplayers" title="User Suggested Number of Players" totalvotes="610">
			
		<results numplayers="1">		
					<result value="Best" numvotes="2" />
					<result value="Recommended" numvotes="16" />
					<result value="Not Recommended" numvotes="336" />
				</results>					
			
		<results numplayers="2">		
					<result value="Best" numvotes="32" />
					<result value="Recommended" numvotes="268" />
					<result value="Not Recommended" numvotes="176" />
				</results>					
			
		<results numplayers="3">		
					<result value="Best" numvotes="86" />
					<result value="Recommended" numvotes="358" />
					<result value="Not Recommended" numvotes="53" />
				</results>					
			
		<results numplayers="4">		
					<result value="Best" numvotes="430" />
					<result value="Recommended" numvotes="117" />
					<result value="Not Recommended" numvotes="8" />
				</results>					
			
		<results numplayers="5">		
					<result value="Best" numvotes="126" />
					<result value="Recommended" numvotes="306" />
					<result value="Not Recommended" numvotes="65" />
				</results>					
			
		<results numplayers="6">		
					<result value="Best" numvotes="267" />
					<result value="Recommended" numvotes="169" />
					<result value="Not Recommended" numvotes="56" />
				</results>					
			
		<results numplayers="6+">		
					<result value="Best" numvotes="11" />
					<result value="Recommended" numvotes="40" />
					<result value="Not Recommended" numvotes="208" />
				</results>					
	</poll> 			               				<playingtime value="180" />
						               				<minplaytime value="60" />
						               				<maxplaytime value="180" />
						               				<minage value="14" />
						      			<poll name="suggested_playerage" title="User Suggested Player Age" totalvotes="171">
			<results>		
					<result value="2" numvotes="1" />
					<result value="3" numvotes="0" />
					<result value="4" numvotes="0" />
					<result value="5" numvotes="0" />
					<result value="6" numvotes="1" />
					<result value="8" numvotes="7" />
					<result value="10" numvotes="20" />
					<result value="12" numvotes="66" />
					<result value="14" numvotes="61" />
					<result value="16" numvotes="15" />
					<result value="18" numvotes="0" />
					<result value="21 and up" numvotes="0" />
				</results>					
	</poll> 			      			<poll name="language_dependence" title="Language Dependence" totalvotes="203">
			
		<results>		
					<result level="91" value="No necessary in-game text" numvotes="133" />
					<result level="92" value="Some necessary text - easily memorized or small crib sheet" numvotes="60" />
					<result level="93" value="Moderate in-game text - needs crib sheet or paste ups" numvotes="8" />
					<result level="94" value="Extensive use of text - massive conversion needed to be playable" numvotes="0" />
					<result level="95" value="Unplayable in another language" numvotes="2" />
				</results>					
	</poll> 			      			 			      				
		 			

			
		
					<link type="boardgamecategory" id="1015" value="Civilization" />
		
									
				
		 			

			
		
					<link type="boardgamecategory" id="1046" value="Fighting" />
		
									
				
		 			

			
		
					<link type="boardgamecategory" id="1016" value="Science Fiction" />
		
									
				
		 			

			
		
					<link type="boardgamecategory" id="1113" value="Space Exploration" />
		
									
				
		 			

			
		
					<link type="boardgamecategory" id="1019" value="Wargame" />
		
									
			

			      				
		 			

			
		
					<link type="boardgamemechanic" id="2080" value="Area Majority / Influence" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2072" value="Dice Rolling" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2676" value="Grid Movement" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2026" value="Hexagon Grid" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2959" value="Map Addition" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2011" value="Modular Board" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2685" value="Player Elimination" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2002" value="Tile Placement" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2079" value="Variable Phase Order" />
		
									
				
		 			

			
		
					<link type="boardgamemechanic" id="2015" value="Variable Player Powers" />
		
									
			

			      				
		 			

			
		
					<link type="boardgamefamily" id="66553" value="Components: Control Boards" />
		
									
				
		 			

			
		
					<link type="boardgamefamily" id="64949" value="Components: Map (Interplanetary or Interstellar scale)" />
		
									
				
		 			

			
		
					<link type="boardgamefamily" id="25158" value="Components: Miniatures" />
		
									
				
		 			

			
		
					<link type="boardgamefamily" id="21459" value="Game: Eclipse (Lautapelit.fi)" />
		
									
				
		 			

			
		
					<link type="boardgamefamily" id="12210" value="Mechanism: 4X" />
		
									
			

			      				
		 			

			
		
					<link type="boardgameexpansion" id="217786" value="Eclipse:  Anticipation of the Elders" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="184256" value="Eclipse: Black Hole" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="136155" value="Eclipse: Elders of the Solstice" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="190742" value="Eclipse: Gift of the Elders" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="152898" value="Eclipse: Minions of the Solstice" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="154785" value="Eclipse: Nebula" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="131415" value="Eclipse: Pulsar" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="125898" value="Eclipse: Rise of the Ancients" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="133967" value="Eclipse: Rise of the Ancients – The Tractor Beam" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="135838" value="Eclipse: Rockets of Celebration" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="179255" value="Eclipse: Shadow of the Rift" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="146690" value="Eclipse: Ship Pack One" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="104746" value="Eclipse: Supernova" />
		
									
				
		 			

			
		
					<link type="boardgameexpansion" id="171114" value="Eclipse: The Galactic North" />
		
									
			

			      			

			      			

			      			

			      			

			      				
		 			

			
		
					<link type="boardgameimplementation" id="246900" value="Eclipse: Second Dawn for the Galaxy" />
		
									
			

			      			

			      	      	      				
		 			

			
		
					<link type="boardgamedesigner" id="13000" value="Touko Tahkokallio" />
		
									
			

			      				
		 			

			
		
					<link type="boardgameartist" id="19023" value="Ossi Hiekkala" />
		
									
				
		 			

			
		
					<link type="boardgameartist" id="32143" value="Sampo Sikiö" />
		
									
			

			      	      				
		 			

			
		
					<link type="boardgamepublisher" id="3218" value="Lautapelit.fi" />
		
									
				
		 			

			
		
					<link type="boardgamepublisher" id="157" value="Asmodee" />
		
									
				
		 			

			
		
					<link type="boardgamepublisher" id="15889" value="Asterion Press" />
		
									
				
		 			

			
		
					<link type="boardgamepublisher" id="8291" value="Korea Boardgames Co., Ltd." />
		
									
				
		 			

			
		
					<link type="boardgamepublisher" id="7466" value="Rebel Sp. z o.o." />
		
									
				
		 			

			
		
					<link type="boardgamepublisher" id="2861" value="Ystari Games" />
		
									
			

			
	

	

	
	
	
   		<statistics page="1">
								<ratings >
			<usersrated value="27208" />
			<average value="7.86486" />
			<bayesaverage value="7.66569" />

			<ranks>
															<rank type="subtype" id="1" name="boardgame" friendlyname="Board Game Rank" value="66" bayesaverage="7.66569" />
																				<rank type="family" id="5497" name="strategygames" friendlyname="Strategy Game Rank" value="57" bayesaverage="7.67472" />
												</ranks>

			<stddev value="1.49482" />
			<median value="0" />
			<owned value="27243" />
			<trading value="802" />
			<wanting value="905" />
			<wishing value="7043" />
			<numcomments value="4929" />
			<numweights value="1916" />
			<averageweight value="3.7015" />
			</ratings>
								</statistics>
     
	
          
</item>
'''

game_soup = BeautifulSoup(xml, features='xml').item