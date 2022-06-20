<script context="module">
    export async function load({params}){
        return {props: {event_id: params.event_id}}
    }
</script>

<script>
    import { supabase } from '$lib/supabaseClient'

    export let event_id

    let loading = true
    let name = null
    let username = ""

    async function getEvent() {
        try {
            loading = true
            let { data, error, status } = await supabase
                .from('events')
                .select("name, organizer_id (username)")
                .eq('id', event_id)
                .single()

            if (error && status !== 406) throw error

            if (data) {
                name = data.name
                username = data.organizer_id.username
            }
        } catch (error) {
            alert(error.message)
        } finally {
            loading = false
        }
    }

    async function updateEvent() {
        try {
            loading = true

            const updates = {
                id: event_id,
                name,
            }

            let { error } = await supabase.from('events').upsert(updates, {
                returning: 'minimal', // Don't return the value after inserting
            })

            if (error) throw error
        } catch (error) {
            alert(error.message)
        } finally {
            loading = false
        }
    }
</script>

<div class="container">
    {username}
    <form use:getEvent class="form-widget" on:submit|preventDefault={updateEvent}>
        <div>
            <label for="name">Name</label>
            <input
                    id="name"
                    type="text"
                    bind:value={name}
            />
        </div>

        <div>
            <input type="submit" class="button block primary" value={loading ? 'Loading ...' : 'Update'} disabled={loading}/>
        </div>
    </form>

</div>
