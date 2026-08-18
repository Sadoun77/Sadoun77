using UnityEngine;
using CastleBusters.Terrain;

namespace CastleBusters.Weapons
{
    /// <summary>
    /// A rocket that flies in a straight line and, on impact, carves a crater
    /// out of any DestructibleTerrain2D it hits before destroying itself.
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D))]
    public class RocketProjectile2D : MonoBehaviour
    {
        [SerializeField] private float explosionRadius = 1.2f;
        [SerializeField] private float launchSpeed = 12f;
        [SerializeField] private GameObject explosionEffectPrefab;

        public void Launch(Vector2 direction)
        {
            GetComponent<Rigidbody2D>().linearVelocity = direction.normalized * launchSpeed;
        }

        private void OnCollisionEnter2D(Collision2D collision)
        {
            Explode(collision.gameObject, collision.GetContact(0).point);
        }

        private void OnTriggerEnter2D(Collider2D other)
        {
            Explode(other.gameObject, transform.position);
        }

        private void Explode(GameObject hitObject, Vector2 impactPoint)
        {
            var terrain = hitObject.GetComponentInParent<DestructibleTerrain2D>();
            if (terrain != null)
            {
                terrain.DestroyCircle(impactPoint, explosionRadius);
            }

            if (explosionEffectPrefab != null)
            {
                Instantiate(explosionEffectPrefab, impactPoint, Quaternion.identity);
            }

            Destroy(gameObject);
        }
    }
}
