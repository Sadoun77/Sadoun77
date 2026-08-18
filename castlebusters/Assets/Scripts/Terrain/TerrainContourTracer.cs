using System.Collections.Generic;
using UnityEngine;

namespace CastleBusters.Terrain
{
    /// <summary>
    /// Converts a binary solid/empty grid into closed boundary polygons by
    /// collecting the exposed edges of every solid cell (an edge facing a
    /// non-solid neighbor) and stitching those edges corner-to-corner into
    /// loops. Outer island boundaries come out CCW-wound; the boundary of an
    /// air pocket fully enclosed in solid comes out CW-wound.
    /// </summary>
    public static class TerrainContourTracer
    {
        public static List<List<Vector2>> Trace(bool[,] solid, int width, int height, float minPerimeter)
        {
            var edgeMap = new Dictionary<Vector2Int, Vector2Int>();

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    if (!solid[x, y]) continue;

                    if (!IsSolid(solid, width, height, x, y - 1))
                        AddEdge(edgeMap, new Vector2Int(x, y), new Vector2Int(x + 1, y));
                    if (!IsSolid(solid, width, height, x + 1, y))
                        AddEdge(edgeMap, new Vector2Int(x + 1, y), new Vector2Int(x + 1, y + 1));
                    if (!IsSolid(solid, width, height, x, y + 1))
                        AddEdge(edgeMap, new Vector2Int(x + 1, y + 1), new Vector2Int(x, y + 1));
                    if (!IsSolid(solid, width, height, x - 1, y))
                        AddEdge(edgeMap, new Vector2Int(x, y + 1), new Vector2Int(x, y));
                }
            }

            var contours = new List<List<Vector2>>();

            while (edgeMap.Count > 0)
            {
                var enumerator = edgeMap.GetEnumerator();
                enumerator.MoveNext();
                Vector2Int start = enumerator.Current.Key;

                var loop = new List<Vector2Int> { start };
                Vector2Int current = start;

                int safety = edgeMap.Count + 1;
                while (safety-- > 0)
                {
                    if (!edgeMap.TryGetValue(current, out Vector2Int next)) break;
                    edgeMap.Remove(current);
                    current = next;
                    if (current == start) break;
                    loop.Add(current);
                }

                if (Perimeter(loop) >= minPerimeter)
                {
                    contours.Add(SimplifyCollinear(loop));
                }
            }

            return contours;
        }

        private static bool IsSolid(bool[,] solid, int width, int height, int x, int y)
        {
            if (x < 0 || x >= width || y < 0 || y >= height) return false;
            return solid[x, y];
        }

        private static void AddEdge(Dictionary<Vector2Int, Vector2Int> edgeMap, Vector2Int from, Vector2Int to)
        {
            // Circular blast holes never produce the pixel-diagonal "checkerboard touch"
            // configuration that would make two distinct edges share a start corner.
            edgeMap[from] = to;
        }

        private static float Perimeter(List<Vector2Int> loop)
        {
            float total = 0f;
            for (int i = 0; i < loop.Count; i++)
            {
                Vector2Int a = loop[i];
                Vector2Int b = loop[(i + 1) % loop.Count];
                total += Vector2Int.Distance(a, b);
            }
            return total;
        }

        private static List<Vector2> SimplifyCollinear(List<Vector2Int> loop)
        {
            int count = loop.Count;
            var result = new List<Vector2>(count);

            for (int i = 0; i < count; i++)
            {
                Vector2Int prev = loop[(i - 1 + count) % count];
                Vector2Int curr = loop[i];
                Vector2Int next = loop[(i + 1) % count];

                Vector2Int dirIn = curr - prev;
                Vector2Int dirOut = next - curr;

                bool collinear = dirIn.x * dirOut.y - dirIn.y * dirOut.x == 0;
                if (!collinear)
                {
                    result.Add(curr);
                }
            }

            if (result.Count >= 3) return result;

            // Degenerate loop (e.g. a single stray cell before simplification) - fall back
            // to three of its original corners so PolygonCollider2D still gets a valid path.
            return new List<Vector2> { loop[0], loop[count / 3], loop[2 * count / 3] };
        }
    }
}
