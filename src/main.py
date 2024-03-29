import math
import pygame
from pygame.locals import *
from pygame import draw
from buttons import Button, ToggleButton
from appModel import Tile, Edge, AppModel, AppState, TileType
from algorithms import enfa2nfa, nfa2dfa, minimize_dfa
from data_structures.epsilon_nfa import EpsilonNFA
from data_structures.nfa import NFA
from data_structures.dfa import DFA

pygame.init()
screen = pygame.display.set_mode((1800, 900), pygame.RESIZABLE)

tiles = [Tile((i * 110, i * 110), i) for i in range(5)]
tilePairs: list[Edge] = []
occupiedIds: set[int] = {tile.id for tile in tiles}
model = AppModel()

buttonWidth, buttonHeight = 180, 50

pairButton = ToggleButton(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="New Delta",
    color=(0, 128, 0),
    toState=AppState.pairing,
)
depairButton = ToggleButton(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="Remove Delta",
    color=(128, 0, 0),
    toState=AppState.depairing,
)
renameButton = ToggleButton(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="Reassign Char",
    color=(0, 0, 128),
    toState=AppState.renamingLabels,
)
setAsStartButton = ToggleButton(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="Set as Start",
    color=(0, 0, 128),
    toState=AppState.setAsStart,
)
setAsFinalButton = ToggleButton(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="Set as Final",
    color=(0, 0, 128),
    toState=AppState.setAsEnd,
)

reanmeStateButton = ToggleButton(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="Rename State",
    color=(0, 0, 128),
    toState=AppState.renamingStates,
)

removeStateButton = ToggleButton(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="Remove State",
    color=(128, 0, 0),
    toState=AppState.removing,
)

appendButton = Button(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="New State",
    color=(0, 128, 0),
)
convertButton = Button(
    left=0,
    top=screen.get_height() - buttonHeight,
    width=buttonWidth,
    height=buttonHeight,
    text="Convert to DFA",
    color=(245, 202, 35),
)

toggleButtons: list[Button] = [
    pairButton,
    depairButton,
    renameButton,
    reanmeStateButton,
    setAsStartButton,
    setAsFinalButton,
    removeStateButton,
]

clickButtons: list[Button] = [appendButton, convertButton]


def arrangeButtons():
    buttonCnt = len(toggleButtons) + len(clickButtons)
    buttonSpacing = (screen.get_width() - (buttonWidth * buttonCnt)) / (buttonCnt - 1)
    for i, button in enumerate(toggleButtons):
        button.left = buttonSpacing * (i) + buttonWidth * i
        button.bottom = screen.get_height()
    for i, button in enumerate(clickButtons):
        button.left = buttonSpacing * (i + len(toggleButtons)) + buttonWidth * (
            i + len(toggleButtons)
        )
        button.bottom = screen.get_height()


arrangeButtons()


def appendNewTile():
    new_tile_id = len(tiles)
    while new_tile_id in occupiedIds:
        new_tile_id += 1
    new_tile = Tile(
        (screen.get_width() // 2 - 50, screen.get_height() // 2 - 50),
        new_tile_id,
    )
    tiles.append(new_tile)
    occupiedIds.add(new_tile_id)


def constructEpsilonNFA() -> EpsilonNFA:
    Q: set[str] = {tile.name for tile in tiles}

    T: set[str] = set()

    for pair in tilePairs:
        for label in pair.labels:
            if label:
                T.add(label)

    delta: dict[tuple[str, str], set[str]] = {}
    for edge in tilePairs:
        for label in edge.labels:
            if (edge.fromTile.name, label) not in delta:
                delta[(edge.fromTile.name, label)] = set()
            delta[(edge.fromTile.name, label)].add(edge.toTile.name)

    q0: str = next(
        (
            tile.name
            for tile in tiles
            if tile.type == TileType.start or tile.type == TileType.start_final
        ),
        "",
    )

    qf: set[str] = {
        tile.name
        for tile in tiles
        if tile.type == TileType.final or tile.type == TileType.start_final
    }
    return EpsilonNFA(Q, T, delta, q0, qf)


def makeId(digKeys: list[str]) -> int:
    strId = "".join(digKeys)
    return int(strId)


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        for tile in tiles:
            if tile.update(event, model):
                break
        for button in toggleButtons:
            button.update(event, model)
        if event.type == QUIT:
            quit()
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            arrangeButtons()
        elif event.type == MOUSEBUTTONDOWN:
            if appendButton.isClicked(event):
                appendNewTile()
            if convertButton.isClicked(event):
                try:
                    e_nfa = constructEpsilonNFA()
                    thenfa = enfa2nfa.transfer_epsilon_nfa_to_nfa(e_nfa)
                    dogwaterdfa = nfa2dfa.transfer_nfa_to_dfa(thenfa)
                    minimized_dfa = minimize_dfa.minimize_dfa(dogwaterdfa)

                    e_nfa.draw("tmp/enfa")
                    thenfa.draw("tmp/nfa")
                    dogwaterdfa.draw("tmp/ddfa")
                    minimized_dfa.draw("tmp/dfa")
                except ValueError:
                    print("Invalid Epsilon NFA definition")
        elif event.type == KEYDOWN:
            if event.unicode == " ":
                model.pressedKeys.append("")
            else:
                model.pressedKeys.append(event.unicode)
    match model.state:
        case AppState.pairing:
            if len(model.selected_tiles) >= 2 and len(model.pressedKeys) >= 1:
                selected_tiles = model.selected_tiles
                selectedPair = Edge(
                    selected_tiles[0], selected_tiles[1], model.pressedKeys[0]
                )
                if tilePairs.count(selectedPair) == 0:
                    tilePairs.append(selectedPair)
                else:
                    selectedPair = tilePairs[tilePairs.index(selectedPair)]
                    selectedPair.addLabel(model.pressedKeys[0])
                model.selected_tiles.clear()
                model.pressedKeys.clear()
        case AppState.depairing:
            if len(model.selected_tiles) >= 2 and len(model.pressedKeys) >= 1:
                selected_tiles = model.selected_tiles
                selectedPair = Edge(selected_tiles[0], selected_tiles[1])
                if tilePairs.count(selectedPair) != 0:
                    selectedPair = tilePairs[tilePairs.index(selectedPair)]
                    selectedPair.removeLabel(model.pressedKeys[0])
                    if selectedPair.isEmpty():
                        tilePairs.remove(selectedPair)
                model.selected_tiles.clear()
                model.pressedKeys.clear()
        case AppState.renamingLabels:
            if len(model.selected_tiles) >= 2 and len(model.pressedKeys) >= 2:
                selected_tiles = model.selected_tiles
                selectedPair = Edge(selected_tiles[0], selected_tiles[1])
                if tilePairs.count(selectedPair) != 0:
                    selectedPair = tilePairs[tilePairs.index(selectedPair)]
                    selectedPair.renameLabel(model.pressedKeys[0], model.pressedKeys[1])
                model.selected_tiles.clear()
                model.pressedKeys.clear()
        case AppState.renamingStates:
            if len(model.selected_tiles) >= 1 and len(model.pressedKeys) >= 2:
                if model.pressedKeys[-1] == "\r":
                    id = makeId(model.pressedKeys[:-1])
                    selected_tile = tiles[tiles.index(model.selected_tiles[0])]
                    if id not in occupiedIds:
                        selected_tile.rename(id)
                        occupiedIds.add(id)
                    else:
                        print("Duplicate ID")
                    model.selected_tiles.clear()
                    model.pressedKeys.clear()
        case AppState.removing:
            if len(model.selected_tiles) >= 1:
                selected_tile = model.selected_tiles[0]
                tiles.remove(selected_tile)
                occupiedIds.remove(selected_tile.id)
                for pair in tilePairs:
                    if pair.fromTile == selected_tile or pair.toTile == selected_tile:
                        tilePairs.remove(pair)
                model.selected_tiles.clear()
        case AppState.setAsStart:
            if len(model.selected_tiles) >= 1:
                for tile in tiles:
                    if tile == model.selected_tiles[0]:
                        continue
                    if tile.type == TileType.start:
                        tile.type = TileType.intermediate
                    elif tile.type == TileType.start_final:
                        tile.type = TileType.final
                selected_tile: Tile = model.selected_tiles[0]
                tile_type = selected_tile.type
                match tile_type:
                    case TileType.final:
                        selected_tile.type = TileType.start_final
                    case TileType.intermediate:
                        selected_tile.type = TileType.start
                    case TileType.start_final:
                        selected_tile.type = TileType.final
                    case TileType.start:
                        selected_tile.type = TileType.intermediate
                model.selected_tiles.clear()
        case AppState.setAsEnd:
            if len(model.selected_tiles) >= 1:
                selected_tile = model.selected_tiles[0]
                tile_type = selected_tile.type
                match tile_type:
                    case TileType.final:
                        selected_tile.type = TileType.intermediate
                    case TileType.start_final:
                        selected_tile.type = TileType.start
                    case TileType.start:
                        selected_tile.type = TileType.start_final
                    case TileType.intermediate:
                        selected_tile.type = TileType.final
                model.selected_tiles.clear()

    screen.fill((255, 255, 255))
    for pair in tilePairs:
        pair.draw(screen=screen)
    for tile in tiles:
        tile.draw(screen)

    for tile in model.selected_tiles:
        pygame.draw.circle(screen, (0, 255, 255), tile.rect.center, 50, 5)

    for button in toggleButtons:
        button.draw(screen, model)
    for button in clickButtons:
        button.draw(screen)
    pygame.display.flip()
    clock.tick(30)
