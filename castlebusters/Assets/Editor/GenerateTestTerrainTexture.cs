#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEngine;

namespace CastleBusters.EditorTools
{
    /// One-click placeholder sand texture so DestructibleTerrain2D has something
    /// to point at before real terrain art exists.
    public static class GenerateTestTerrainTexture
    {
        [MenuItem("Tools/Castle Busters/Generate Test Terrain Texture")]
        public static void Generate()
        {
            const int width = 256;
            const int height = 128;

            var texture = new Texture2D(width, height, TextureFormat.RGBA32, false);
            var pixels = new Color32[width * height];
            var solid = new Color32(194, 178, 128, 255);
            var empty = new Color32(0, 0, 0, 0);

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    pixels[y * width + x] = y < height * 0.75f ? solid : empty;
                }
            }

            texture.SetPixels32(pixels);
            texture.Apply();

            const string directory = "Assets/Textures";
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            string path = directory + "/TestSandTerrain.png";
            File.WriteAllBytes(path, texture.EncodeToPNG());
            AssetDatabase.ImportAsset(path);

            var importer = (TextureImporter)AssetImporter.GetAtPath(path);
            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Single;
            importer.filterMode = FilterMode.Point;
            importer.SaveAndReimport();

            Debug.Log($"Generated test terrain texture at {path}");
        }
    }
}
#endif
