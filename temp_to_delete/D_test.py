def is_on_slider(px, py, x1, y1, x2, y2):
    cross = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    if abs(cross) > 1e-9:
        return False
    return (min(x1, x2) <= px <= max(x1, x2) and 
            min(y1, y2) <= py <= max(y1, y2))

def find_intersecting_slider(ball_x, ball_y, sliders):
    for i, ((x1, y1), (x2, y2)) in enumerate(sliders):
        if is_on_slider(ball_x, ball_y, x1, y1, x2, y2):
            return i
    return None

def find_vertical_intersection(ball_x, ball_y, sliders):
    best_intersection = None
    best_y = -1
    
    for i, ((x1, y1), (x2, y2)) in enumerate(sliders):
        if not (min(x1, x2) <= ball_x <= max(x1, x2)) or x2 == x1:
            continue
        
        m = (y2 - y1) / (x2 - x1)
        y_intersect = y1 + m * (ball_x - x1)
        
        if (0 <= y_intersect < ball_y and y_intersect > best_y and
            min(y1, y2) <= y_intersect <= max(y1, y2)):
            best_y = y_intersect
            best_intersection = (i, ball_x, y_intersect)
    
    return best_intersection

def is_stuck_at_intersection(ball_x, ball_y, sliders):
    intersecting = [i for i, ((x1, y1), (x2, y2)) in enumerate(sliders)
                   if is_on_slider(ball_x, ball_y, x1, y1, x2, y2)]
    
    if len(intersecting) >= 2:
        for i in intersecting:
            (x1, y1), (x2, y2) = sliders[i]
            if (ball_x == x1 and ball_y == y1) or (ball_x == x2 and ball_y == y2):
                return True
    return False

def get_direction(x1, y1, x2, y2, cx, cy):
    if y1 < y2:
        tx, ty = x1, y1
    elif y2 < y1:
        tx, ty = x2, y2
    else:
        return 0, -1
    
    dx = 1 if tx > cx else -1 if tx < cx else 0
    dy = 1 if ty > cy else -1 if ty < cy else 0
    
    return (0, -1) if dx == 0 and dy == 0 else (dx, dy)

n = int(input())
sliders = []
for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    sliders.append(((x1, y1), (x2, y2)))

ball_x, ball_y = map(int, input().split())
visited = set()

while ball_y > 0 and (ball_x, ball_y) not in visited:
    visited.add((ball_x, ball_y))
    
    if is_stuck_at_intersection(ball_x, ball_y, sliders):
        break
    
    slider_idx = find_intersecting_slider(ball_x, ball_y, sliders)
    
    if slider_idx is not None:
        (x1, y1), (x2, y2) = sliders[slider_idx]
        dx, dy = get_direction(x1, y1, x2, y2, ball_x, ball_y)
        
        if dx == 0 and dy == -1:
            intersection = find_vertical_intersection(ball_x, ball_y, sliders)
            if intersection:
                _, ball_x, ball_y = intersection
            else:
                ball_y -= 1
        else:
            ball_x += dx
            ball_y += dy
    else:
        intersection = find_vertical_intersection(ball_x, ball_y, sliders)
        if intersection:
            _, ball_x, ball_y = intersection
        else:
            ball_y -= 1

print(int(ball_x), int(ball_y))