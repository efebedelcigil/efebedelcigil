"""Lightweight board-surface treatment derived from current package geometry."""
from contribution_routing import land_bounds

def surface_regions(geometry,cells,days):
 regions=[]
 for date,level in sorted(days.items()):
  if not level:continue
  cell=cells[date];l,t,r,b=land_bounds(geometry,cell,level)
  regions.append({'date':date,'ellipse':((l+r)/2,(t+b)/2,(r-l)/2+3,(b-t)/2+2)})
 return regions

def surface_art(geometry,cells,days,theme):
 regions=surface_regions(geometry,cells,days)
 definitions=['<defs><radialGradient id="pcbTraceQuiet"><stop stop-color="black" stop-opacity=".78"/><stop offset=".45" stop-color="black" stop-opacity=".48"/><stop offset="1" stop-color="black" stop-opacity="0"/></radialGradient>', '<radialGradient id="pcbContactShade"><stop stop-color="'+('#071c13' if theme=='dark' else '#173c29')+'" stop-opacity=".48"/><stop offset=".45" stop-color="'+('#071c13' if theme=='dark' else '#173c29')+'" stop-opacity=".22"/><stop offset="1" stop-color="'+('#071c13' if theme=='dark' else '#173c29')+'" stop-opacity="0"/></radialGradient>',f'<mask id="pcbTraceQuietMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{geometry.width}" height="{geometry.height}"><rect width="{geometry.width}" height="{geometry.height}" fill="white"/>']
 shadows=['<g data-contact-shadows="true">']
 for region in regions:
  x,y,rx,ry=region['ellipse']
  definitions.append(f'<ellipse data-trace-quiet="{region["date"]}" cx="{x}" cy="{y}" rx="{rx*1.35}" ry="{ry*1.35}" fill="url(#pcbTraceQuiet)"/>')
  shadows.append(f'<ellipse data-contact-shadow="{region["date"]}" cx="{x+.6}" cy="{y+.8}" rx="{rx}" ry="{ry}" fill="url(#pcbContactShade)"/>')
 definitions.append('</mask></defs>');shadows.append('</g>')
 return ''.join(definitions),''.join(shadows)
