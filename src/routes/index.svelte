<script>
    import {user} from "$lib/sessionStore"
    import {supabase} from "$lib/supabaseClient"
    import Profile from "$lib/Profile.svelte"
    import Auth from "$lib/Auth.svelte"

    user.set(supabase.auth.user())

    supabase.auth.onAuthStateChange((_, session) => {
        user.set(session.user)
    })
</script>

{#if $user}
    <Profile />
{:else}
    <Auth />
{/if}

