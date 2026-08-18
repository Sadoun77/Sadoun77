using System.Collections;
using UnityEngine;

namespace CastleBusters.Terrain
{
    /// <summary>
    /// A 2D sand-terrain block that can be blown apart by explosions.
    /// The terrain's shape lives in a mutable Texture2D (alpha = solid vs empty);
    /// destroying a circle clears alpha in that region and regenerates a
    /// PolygonCollider2D from the surviving pixels so physics matches the sprite.
    /// </summary>
    [RequireComponent(typeof(PolygonCollider2D))]
    [RequireComponent(typeof(SpriteRenderer))]
    public class DestructibleTerrain2D : MonoBehaviour
    {
        [Header("Terrain Bitmap")]
        [Tooltip("Source terrain shape. Alpha channel defines solid (>0) vs empty (0) pixels.")]
        [SerializeField] private Texture2D sourceTexture;
        [SerializeField] private float pixelsPerUnit = 100f;

        [Header("Destruction")]
        [SerializeField] private byte solidAlphaThreshold = 32;
        [Tooltip("Sample every Nth pixel when rebuilding the collider. Higher = cheaper but blockier.")]
        [SerializeField, Range(1, 4)] private int colliderGridStep = 2;
        [SerializeField] private float minColliderContourPerimeter = 4f;

        private Texture2D _workingTexture;
        private SpriteRenderer _spriteRenderer;
        private PolygonCollider2D _polygonCollider;
        private Color32[] _pixels;
        private int _width;
        private int _height;
        private bool _colliderRebuildQueued;

        private void Awake()
        {
            _spriteRenderer = GetComponent<SpriteRenderer>();
            _polygonCollider = GetComponent<PolygonCollider2D>();
            InitializeTexture();
            RebuildCollider();
        }

        private void InitializeTexture()
        {
            _workingTexture = new Texture2D(sourceTexture.width, sourceTexture.height, TextureFormat.RGBA32, false)
            {
                filterMode = FilterMode.Point
            };
            _workingTexture.SetPixels32(sourceTexture.GetPixels32());
            _workingTexture.Apply();

            _width = _workingTexture.width;
            _height = _workingTexture.height;
            _pixels = _workingTexture.GetPixels32();

            _spriteRenderer.sprite = Sprite.Create(
                _workingTexture,
                new Rect(0, 0, _width, _height),
                new Vector2(0.5f, 0.5f),
                pixelsPerUnit);
        }

        /// Punches a circular hole in the terrain at a world-space position.
        public void DestroyCircle(Vector2 worldPosition, float radiusWorld)
        {
            Vector2 local = transform.InverseTransformPoint(worldPosition);
            Vector2 pixelCenter = LocalToPixel(local);
            float radiusPixels = radiusWorld * pixelsPerUnit;

            int minX = Mathf.Clamp(Mathf.FloorToInt(pixelCenter.x - radiusPixels), 0, _width - 1);
            int maxX = Mathf.Clamp(Mathf.CeilToInt(pixelCenter.x + radiusPixels), 0, _width - 1);
            int minY = Mathf.Clamp(Mathf.FloorToInt(pixelCenter.y - radiusPixels), 0, _height - 1);
            int maxY = Mathf.Clamp(Mathf.CeilToInt(pixelCenter.y + radiusPixels), 0, _height - 1);

            float sqrRadius = radiusPixels * radiusPixels;
            bool changed = false;

            for (int y = minY; y <= maxY; y++)
            {
                for (int x = minX; x <= maxX; x++)
                {
                    float dx = x - pixelCenter.x;
                    float dy = y - pixelCenter.y;
                    if (dx * dx + dy * dy > sqrRadius) continue;

                    int index = y * _width + x;
                    if (_pixels[index].a == 0) continue;
                    _pixels[index].a = 0;
                    changed = true;
                }
            }

            if (!changed) return;

            _workingTexture.SetPixels32(_pixels);
            _workingTexture.Apply();
            QueueColliderRebuild();
        }

        private Vector2 LocalToPixel(Vector2 local)
        {
            float px = local.x * pixelsPerUnit + _width * 0.5f;
            float py = local.y * pixelsPerUnit + _height * 0.5f;
            return new Vector2(px, py);
        }

        private Vector2 PixelToLocal(float px, float py)
        {
            float x = (px - _width * 0.5f) / pixelsPerUnit;
            float y = (py - _height * 0.5f) / pixelsPerUnit;
            return new Vector2(x, y);
        }

        private void QueueColliderRebuild()
        {
            if (_colliderRebuildQueued) return;
            _colliderRebuildQueued = true;
            StartCoroutine(RebuildColliderNextFrame());
        }

        private IEnumerator RebuildColliderNextFrame()
        {
            yield return null; // batches same-frame explosions into a single rebuild
            _colliderRebuildQueued = false;
            RebuildCollider();
        }

        private void RebuildCollider()
        {
            int gridW = Mathf.Max(1, _width / colliderGridStep);
            int gridH = Mathf.Max(1, _height / colliderGridStep);
            var solid = new bool[gridW, gridH];

            for (int gy = 0; gy < gridH; gy++)
            {
                for (int gx = 0; gx < gridW; gx++)
                {
                    solid[gx, gy] = SampleSolid(gx * colliderGridStep, gy * colliderGridStep);
                }
            }

            var contours = TerrainContourTracer.Trace(solid, gridW, gridH, minColliderContourPerimeter);

            _polygonCollider.pathCount = contours.Count;
            for (int i = 0; i < contours.Count; i++)
            {
                var contour = contours[i];
                var path = new Vector2[contour.Count];
                for (int p = 0; p < contour.Count; p++)
                {
                    float px = contour[p].x * colliderGridStep;
                    float py = contour[p].y * colliderGridStep;
                    path[p] = PixelToLocal(px, py);
                }
                _polygonCollider.SetPath(i, path);
            }
        }

        private bool SampleSolid(int px, int py)
        {
            px = Mathf.Clamp(px, 0, _width - 1);
            py = Mathf.Clamp(py, 0, _height - 1);
            return _pixels[py * _width + px].a >= solidAlphaThreshold;
        }
    }
}
