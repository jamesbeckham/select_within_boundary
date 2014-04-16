import rhinoscriptsyntax as rs

###############################################################################
##            FUNCTIONS
###############################################################################

###############################################
##  select_within_boundary  ##
def select_within_boundary(circles_to_filter, circle_radius, closed_crv, plane):
    
    rs.EnableRedraw(False)
    
    ## make a bounding box
    box = rs.BoundingBox(closed_crv, plane)
    planar_rect = rs.AddSrfPt([box[0], box[1], box[2], box[3]])


    ## Project the closed curve on the planar rectangle
    vec_project = rs.VectorCreate(box[0], box[4])
    projected_crv = rs.ProjectCurveToSurface(closed_crv, planar_rect, vec_project)

    ## Offset the curve according to the radius of the circles_to_be_filtered
    vec_offset = rs.VectorCreate(box[4], box[0])
    offset_close_crv = rs.OffsetCurve(projected_crv, vec_offset, 1.0)


    ## Get the hight of the extrusion
    height = rs.Distance(box[0], box[4])

    ## Extrude curve to solid
    base_srf = rs.AddPlanarSrf(offset_close_crv)
    extrude_path = rs.AddLine(box[0], box[4])
    solid = rs.ExtrudeSurface(base_srf, extrude_path)

    ## Check the center of the circles_to_be_filtered in the solid
    for circle in circles_to_filter:
        circle_box = rs.BoundingBox(circle, plane)
        diagonal = rs.AddLine(circle_box[0], circle_box[6])
        center = rs.CurveMidPoint(diagonal)
        if rs.IsPointInSurface(solid, center):
            circle_in_solid.append(circle)

        rs.DeleteObject(diagonal)
        

    ## Delete all temporary objects
    rs.DeleteObject(planar_rect)
    rs.DeleteObject(projected_crv)
    rs.DeleteObject(offset_close_crv)
    rs.DeleteObject(base_srf)
    rs.DeleteObject(extrude_path)
    rs.DeleteObject(solid)
    rs.DeleteObject(solid)




###############################################################################
##            MAIN
###############################################################################




## Select the closed curves
closed_crvs = rs.GetObjects("Select the closed curves", rs.filter.curve)


## Check if all closed_crvs are closed, highlight(select) the not closed curves
non_closed_crvs = []
for crv in closed_crvs:
    if not rs.IsCurveClosed(crv):
        non_closed_crvs.append(crv)
if len(non_closed_crvs) > 0:
    rs.SelectObjects(non_closed_crvs)
else:
    rs.LockObjects(closed_crvs)

    ## Select the circles to be filter
    circles_to_filter = rs.GetObjects("Select the circles to be filter", rs.filter.curve)

    rs.UnlockObjects(closed_crvs)

    ## Get the circle radius from user
    circle_radius = rs.GetReal("What is the radius of the circles to be filtered?", 1)

    ## Get the plane of the closed curve
    plane_origin, plane_x, plane_y = rs.GetPoints(
                                                    message1 = "On the pre-drawn rectangle, please select the origin(usually the lower-left corner)", 
                                                    message2 = "Select the points showing x-direction and y-direction", 
                                                    max_points = 3
    )
 
    plane = rs.PlaneFromPoints(plane_origin, plane_x, plane_y)

    circle_in_solid = []

    for closed_crv in closed_crvs:
        select_within_boundary(circles_to_filter, circle_radius, closed_crv, plane)

    ## Add to selection
    selection = rs.SelectObjects(circle_in_solid)

rs.EnableRedraw(True)





