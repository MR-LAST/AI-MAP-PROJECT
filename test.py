import pygame
import math
import heapq
import threading

# Step 1: Initialize Pygame
pygame.init()

# Step 2: Define Key Points
key_points = {
    'Library': (913.067, 675.260),
    'Clinic': (318.605, 642),
    'Classroom A': (1337.014, 564.125),
    'Main Gate': (1123.918, -235.594),
}

# Step 3: Create Graph Representation
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

graph = {
    'Library': {'Clinic': calculate_distance(key_points['Library'], key_points['Clinic']),
                'Classroom A': calculate_distance(key_points['Library'], key_points['Classroom A'])},
    'Clinic': {'Library': calculate_distance(key_points['Clinic'], key_points['Library']),
               'Main Gate': calculate_distance(key_points['Clinic'], key_points['Main Gate'])},
    'Classroom A': {'Library': calculate_distance(key_points['Classroom A'], key_points['Library']),
                    'Main Gate': calculate_distance(key_points['Classroom A'], key_points['Main Gate'])},
    'Main Gate': {'Clinic': calculate_distance(key_points['Main Gate'], key_points['Clinic']),
                  'Classroom A': calculate_distance(key_points['Main Gate'], key_points['Classroom A'])},
}

# Step 4: Implement A*
def heuristic(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def a_star(graph, start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
    costs = {start: 0}
    came_from = {start: None}
    
    while queue:
        current_cost, current_node = heapq.heappop(queue)
        if current_node == goal:
            break
        
        for neighbor, distance in graph[current_node].items():
            new_cost = costs[current_node] + distance
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                priority = new_cost + heuristic(key_points[goal], key_points[neighbor])
                heapq.heappush(queue, (priority, neighbor))
                came_from[neighbor] = current_node

    path = []
    while goal:
        path.append(goal)
        goal = came_from[goal]
    
    return path[::-1]

# Step 5: Visualize the Path
def move_character(path, zoom_scale):
    global character_pos, path_drawn
    for point in path:
        while character_pos != list(key_points[point]):
            character_pos[0] = character_pos[0] + (1 if character_pos[0] < key_points[point][0] else -1)
            character_pos[1] = character_pos[1] + (1 if character_pos[1] < key_points[point][1] else -1)
            path_drawn.append(tuple(character_pos))
            pygame.time.delay(10)  # Control the speed of animation

# Step 6: Main Function
def main():
    global character_pos, path_drawn
    character_pos = list(key_points['Library'])  # Start position of the character
    path_drawn = []

    screen_width, screen_height = 1600, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("AI Pathfinding Visualization")
    
    # Load the map image and scale it
    map_image = pygame.image.load("map.png")
    original_map_image = map_image  # Save the original for resizing
    zoom_scale = 1.0
    
    # Input box and button initialization
    input_box_start = pygame.Rect(100, 100, 140, 32)
    input_box_goal = pygame.Rect(100, 150, 140, 32)
    zoom_in_button = pygame.Rect(100, 200, 70, 30)
    zoom_out_button = pygame.Rect(180, 200, 70, 30)

    color_start = pygame.Color('lightskyblue3')
    color_goal = pygame.Color('lightskyblue3')
    color_text_inactive = pygame.Color('lightskyblue3')
    color_text_active = pygame.Color('white')
    color_button = pygame.Color('black')

    active_start = False
    active_goal = False
    text_start = ''
    text_goal = ''

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle input box events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_start.collidepoint(event.pos):
                    active_start = not active_start
                else:
                    active_start = False
                if input_box_goal.collidepoint(event.pos):
                    active_goal = not active_goal
                else:
                    active_goal = False

            if event.type == pygame.KEYDOWN:
                if active_start:
                    if event.key == pygame.K_RETURN:
                        start = text_start
                        path = a_star(graph, start, text_goal)  # Calculate path
                        threading.Thread(target=move_character, args=(path, zoom_scale)).start()
                        text_start = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_start = text_start[:-1]
                    else:
                        text_start += event.unicode
                
                if active_goal:
                    if event.key == pygame.K_RETURN:
                        goal = text_goal
                        path = a_star(graph, text_start, goal)  # Calculate path
                        threading.Thread(target=move_character, args=(path, zoom_scale)).start()
                        text_goal = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_goal = text_goal[:-1]
                    else:
                        text_goal += event.unicode

            # Zoom functionality
            if event.type == pygame.MOUSEBUTTONDOWN:
                if zoom_in_button.collidepoint(event.pos):
                    zoom_scale += 0.1  # Zoom in
                elif zoom_out_button.collidepoint(event.pos):
                    zoom_scale = max(0.1, zoom_scale - 0.1)  # Zoom out, preventing negative scale
        
        # Clear screen
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Scale and draw the map
        scaled_map = pygame.transform.scale(original_map_image, (int(original_map_image.get_width() * zoom_scale), int(original_map_image.get_height() * zoom_scale)))
        screen.blit(scaled_map, (0, 0))

        # Draw text input boxes
        pygame.draw.rect(screen, color_button, input_box_start)
        pygame.draw.rect(screen, color_button, input_box_goal)
        text_surface_start = pygame.font.Font(None, 32).render(text_start, True, color_text_active if active_start else color_text_inactive)
        text_surface_goal = pygame.font.Font(None, 32).render(text_goal, True, color_text_active if active_goal else color_text_inactive)
        screen.blit(text_surface_start, (input_box_start.x + 5, input_box_start.y + 5))
        screen.blit(text_surface_goal, (input_box_goal.x + 5, input_box_goal.y + 5))

        # Draw zoom buttons
        pygame.draw.rect(screen, color_button, zoom_in_button)
        pygame.draw.rect(screen, color_button, zoom_out_button)
        font = pygame.font.Font(None, 24)
        screen.blit(font.render("Zoom In", True, (255, 255, 255)), (zoom_in_button.x + 10, zoom_in_button.y + 5))
        screen.blit(font.render("Zoom Out", True, (255, 255, 255)), (zoom_out_button.x + 10, zoom_out_button.y + 5))

        # Draw the path if available
        for point in path_drawn:
            pygame.draw.circle(screen, (0, 0, 255), (int(point[0]), int(point[1])), 3)  # Draw character path

        # Draw character position
        pygame.draw.circle(screen, (0, 255, 0), (int(character_pos[0]), int(character_pos[1])), 10)  # Character color (e.g., green)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
